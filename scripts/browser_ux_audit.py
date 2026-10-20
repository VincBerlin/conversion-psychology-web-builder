#!/usr/bin/env python3
"""Bounded, observational Playwright UX audit of explicitly authorized public pages.

The browser can execute page JS and GETs can have server-side effects; this is not an
absolute read-only security boundary. Run on local/staging targets when possible.
"""
from __future__ import annotations

import argparse
import ipaddress
import json
from pathlib import Path
import re
import socket
import sys
from urllib.parse import urlsplit, unquote, urljoin

VIEWPORTS = {"desktop": {"width": 1440, "height": 900}, "mobile": {"width": 390, "height": 844}}
MAX_PAGES = 3
MAX_BLOCKED_SAMPLES = 12


def origin_of(url: str) -> str:
    p = urlsplit(url)
    if p.username or p.password or not p.hostname or p.scheme not in ("http", "https"):
        raise ValueError("only http(s) URLs without credentials are allowed")
    if p.hostname.lower() in ("localhost", "127.0.0.1", "::1"):
        pass
    elif p.scheme != "https":
        raise ValueError("remote sites require https")
    return f"{p.scheme}://{p.netloc.lower()}"


def check_target(url: str, remote_public: bool) -> tuple[str, str]:
    p = urlsplit(url)
    origin = origin_of(url)
    if p.query or p.fragment:
        raise ValueError("query strings and fragments are not allowed in the audit target")
    if p.hostname.lower() in ("localhost", "127.0.0.1", "::1"):
        return origin, p.path or "/"
    if not remote_public:
        raise ValueError("remote site requires explicit --remote-public authorization")
    # Best-effort guard. DNS rebinding and redirect-based SSRF still need network isolation.
    try:
        resolved = socket.getaddrinfo(p.hostname, p.port or 443, type=socket.SOCK_STREAM)
    except OSError as exc:
        raise ValueError("cannot resolve remote host") from exc
    for result in resolved:
        ip = ipaddress.ip_address(result[4][0])
        if not ip.is_global:
            raise ValueError("remote target resolves to private/reserved IP; prohibited")
    return origin, p.path or "/"


def normalized_path(path: str) -> str:
    if not path.startswith("/") or path.startswith("//") or "\\" in path or "?" in path or "#" in path:
        raise ValueError("paths must be clean origin-relative URLs without query/fragment")
    decoded = path
    for _ in range(4):
        unescaped = unquote(decoded)
        if unescaped == decoded: break
        decoded = unescaped
    if ".." in decoded.split("/") or decoded.startswith("//") or "\\" in decoded:
        raise ValueError("path traversal disallowed")
    if not re.fullmatch(r"/[A-Za-z0-9_~/%+.,=:@!$&'()*;\-]*", path):
        raise ValueError("path contains invalid characters")
    return path


def policy_for_request(request_url: str, method: str, permitted_origin: str) -> str:
    """Conservative routing policy, also used by side-effect-free unit tests."""
    if method.upper() not in ("GET", "HEAD"):
        return "BLOCK_WRITE_METHOD"
    try:
        if origin_of(request_url) != permitted_origin:
            return "BLOCK_CROSS_ORIGIN"
    except ValueError:
        return "BLOCK_NON_HTTP"
    return "ALLOW"


DOM_READ_JS = r"""() => {
 const clip = (s, n=150) => String(s||'').trim().replace(/\s+/g, ' ').slice(0,n);
 const rect = el => { const r=el.getBoundingClientRect(); return {
  x:Math.round(r.x), y:Math.round(r.y), w:Math.round(r.width), h:Math.round(r.height),
  inViewport: r.bottom>0 && r.top<innerHeight && r.right>0 && r.left<innerWidth,
  visible: !!(r.width && r.height && getComputedStyle(el).visibility!=='hidden' && getComputedStyle(el).display!=='none')
 }; };
 const headings = [...document.querySelectorAll('h1,h2')].slice(0,14).map(e=>({tag:e.tagName.toLowerCase(),text:clip(e.innerText),rect:rect(e)}));
 const actions = [...document.querySelectorAll('a,button,input[type="submit"]')].slice(0,100).map(e=>({
  tag:e.tagName.toLowerCase(),text:clip(e.innerText||e.value||e.getAttribute('aria-label'),100),
  href:e.tagName==='A'?clip(e.getAttribute('href'),250):null,
  type:e.getAttribute('type'),rect:rect(e)
 })).filter(e=>/anfrag|kontakt|termin|angebot|buchen|start|demo|kaufen|kasse|bestell|reserv|contact|book|buy|trial|sign up|get started|request|subscribe|schedule/i.test(e.text)||e.tag==='button'||e.type==='submit').slice(0,24);
 const alerts = [...document.querySelectorAll('[role="alert"],[aria-live="assertive"]')].filter(e=>rect(e).visible).slice(0,12).map(e=>clip(e.innerText,130));
 const forms = [...document.querySelectorAll('form')].slice(0,10).map(f=>({
  action:clip(f.getAttribute('action'),120),method:clip(f.getAttribute('method')||'GET',15),
  fields:[...f.querySelectorAll('input,select,textarea')].slice(0,35).map(e=>{
   const id=e.id; const label= id?document.querySelector(`label[for="${CSS.escape(id)}"]`):null;
   return {tag:e.tagName.toLowerCase(),type:clip(e.getAttribute('type'),25),required:e.required,
     labelled: !!(clip(e.getAttribute('aria-label'))||clip(e.getAttribute('aria-labelledby'))||clip(label?.innerText)||clip(e.closest('label')?.innerText)),
     autocomplete:clip(e.getAttribute('autocomplete'),40),ariaInvalid:e.getAttribute('aria-invalid')};
  })
 }));
 return { title:clip(document.title,160),headings,actions,forms,alerts,
  overflow_x_px:Math.max(0,Math.ceil(document.documentElement.scrollWidth-innerWidth)),
  viewport:{width:innerWidth,height:innerHeight},
  live_validation_tested:false,
  note:'Visibility/label heuristics only; no form submission or user comprehension testing.'
 };
}"""


def make_findings(data: dict, device: str) -> list[dict]:
    """Potential issues are review hypotheses, never measured conversion effects."""
    issues = []
    h1s = [h for h in data.get("headings", []) if h.get("tag") == "h1"]
    if not h1s:
        issues.append({"id": "HEADING_MISSING", "severity": "review", "observation": "No h1 found", "status": "OBSERVED"})
    elif not any(h.get("rect", {}).get("inViewport") for h in h1s):
        issues.append({"id": "HERO_OUT_OF_VIEW", "severity": "review", "observation": "h1 outside initial viewport", "status": "OBSERVED"})
    if data.get("overflow_x_px", 0) > 4:
        issues.append({"id": "HORIZONTAL_OVERFLOW", "severity": "review", "observation": f"{data['overflow_x_px']}px horizontal overflow on {device}", "status": "OBSERVED"})
    if not any(a.get("rect", {}).get("inViewport") and a.get("rect", {}).get("visible") for a in data.get("actions", [])):
        issues.append({"id": "NO_VISIBLE_CTA_CANDIDATE", "severity": "hypothesis", "observation": "No detected action candidate in initial viewport", "status": "HEURISTIC"})
    if device == "mobile":
        tiny = [a.get("text", "") for a in data.get("actions", []) if a.get("rect", {}).get("visible") and min(a.get("rect", {}).get("w", 0), a.get("rect", {}).get("h", 0)) < 24]
        if tiny:
            issues.append({"id": "SMALL_ACTION_TARGET", "severity": "review", "observation": f"{len(tiny)} candidate targets smaller than 24px in at least one dimension; assess WCAG exceptions", "status": "HEURISTIC"})
    unlabelled = sum(1 for f in data.get("forms", []) for field in f.get("fields", []) if field.get("type") not in ("hidden", "submit", "button") and not field.get("labelled"))
    if unlabelled:
        issues.append({"id": "FORM_LABEL_REVIEW", "severity": "review", "observation": f"{unlabelled} potentially unlabelled fields", "status": "HEURISTIC"})
    return issues


def run_audit(url: str, paths: list[str], output: Path, remote_public: bool, chrome_path: str | None = None) -> dict:
    origin, _ = check_target(url, remote_public)
    selected = list(dict.fromkeys(normalized_path(x) for x in paths))
    if not 1 <= len(selected) <= MAX_PAGES:
        raise ValueError(f"between one and {MAX_PAGES} explicitly approved paths required")
    from playwright.sync_api import sync_playwright  # optional dependency, imported only when used
    output.mkdir(parents=True, exist_ok=True)
    report = {
        "status": "RUNNING", "target_origin": origin, "paths": selected, "devices": list(VIEWPORTS),
        "scope": "OBSERVATIONAL_ONLY", "network_policy": "GET/HEAD same-origin only; service workers blocked; no UI actions",
        "critical_caveat": "JavaScript and GET requests can have server-side effects; this is not a sandbox or a guaranteed zero-side-effect mode.",
        "not_tested": ["form submission", "checkout/payment", "click-through interaction", "error-state interactions", "human comprehension", "conversion-rate impact", "accessibility compliance"],
        "blocked_requests": {}, "blocked_request_samples": [], "pages": [], "browser_e2e": "NOT_RUN"
    }
    with sync_playwright() as p:
        launch = {"headless": True}
        if chrome_path:
            launch["executable_path"] = chrome_path
        browser = p.chromium.launch(**launch)
        try:
            for device, viewport in VIEWPORTS.items():
                context = browser.new_context(viewport=viewport, device_scale_factor=1, is_mobile=(device=="mobile"),
                                              has_touch=(device=="mobile"), service_workers="block",
                                              accept_downloads=False, java_script_enabled=True,
                                              ignore_https_errors=False)
                def protect(route):
                    reason = policy_for_request(route.request.url, route.request.method, origin)
                    if reason != "ALLOW":
                        report["blocked_requests"][reason] = report["blocked_requests"].get(reason, 0) + 1
                        if len(report["blocked_request_samples"]) < MAX_BLOCKED_SAMPLES:
                            report["blocked_request_samples"].append({"reason":reason,"method":route.request.method, "url_origin":safe_origin(route.request.url)})
                        route.abort()
                    else:
                        try:
                            # Playwright's route.continue_ follows redirects without rerunning the handler.
                            # Fetch exactly one hop and deny 3xx responses to keep the origin boundary.
                            response = route.fetch(max_redirects=0, timeout=12000)
                            if 300 <= response.status < 400:
                                report["blocked_requests"]["BLOCK_REDIRECT"] = report["blocked_requests"].get("BLOCK_REDIRECT", 0) + 1
                                route.fulfill(status=403, body="Redirect suppressed by observational audit")
                            else:
                                route.fulfill(response=response)
                        except Exception:
                            report["blocked_requests"]["BLOCK_NETWORK_ERROR"] = report["blocked_requests"].get("BLOCK_NETWORK_ERROR", 0) + 1
                            route.abort()
                context.route("**/*", protect)
                # WebSockets can carry writes and do not pass ordinary request routes.
                context.route_web_socket("**/*", lambda ws: ws.close())
                page = context.new_page()
                page.set_default_navigation_timeout(12000)
                page.on("dialog", lambda d: d.dismiss())
                errors=[]
                page.on("pageerror", lambda e: errors.append(str(e)[:200]) if len(errors)<8 else None)
                page.on("console", lambda m: errors.append(m.text[:200]) if m.type=="error" and len(errors)<8 else None)
                for index, path in enumerate(selected):
                    dest = origin + path
                    entry={"device":device,"path":path,"url":dest,"result":"NOT_TESTED","errors":[]}
                    try:
                        response = page.goto(dest, wait_until="domcontentloaded", timeout=12000)
                        page.wait_for_timeout(550)
                        entry["http_status"] = response.status if response else None
                        entry["result"] = "OBSERVED" if response and response.ok else "HTTP_ERROR"
                        entry["data"] = page.evaluate(DOM_READ_JS)
                        entry["issues"] = make_findings(entry["data"],device)
                        for action in entry["data"]["actions"]:
                            href = action.get("href") or ""
                            if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
                                action["destination_check"] = "NOT_NAVIGATION_OR_OUT_OF_SCOPE"
                            else:
                                try:
                                    target = urlsplit(urljoin(dest, href))
                                    if origin_of(target.geturl()) != origin:
                                        action["destination_check"] = "EXTERNAL_NOT_VISITED"
                                    elif (target.path or "/") in selected and not target.query:
                                        action["destination_check"] = "APPROVED_PAGE_TO_OBSERVE"
                                    else:
                                        action["destination_check"] = "SAME_ORIGIN_NOT_VISITED"
                                except ValueError:
                                    action["destination_check"] = "UNRESOLVED_OR_UNSAFE"
                        filename=f"{device}-{index+1}.png"
                        page.screenshot(path=str(output/filename), full_page=False, timeout=7000)
                        entry["screenshot"] = filename
                        entry["js_errors"] = errors[:8]
                    except Exception as exc:
                        entry["result"]="NOT_TESTED"
                        entry["errors"]=[type(exc).__name__ + ': ' + str(exc)[:240]]
                    report["pages"].append(entry)
                    errors.clear()
                context.close()
        finally:
            browser.close()
    successes = sum(page["result"]=="OBSERVED" for page in report["pages"])
    report["status"] = "COMPLETE" if successes==len(report["pages"]) else ("PARTIAL" if successes else "NOT_TESTED")
    report["browser_e2e"] = "EXECUTED" if successes else "NOT_TESTED"
    (output/"browser-ux-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return report


def safe_origin(url: str) -> str:
    try:
        return origin_of(url)
    except ValueError:
        return "non_http_or_invalid"


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--url", required=True, help="Authorized local preview or explicit public URL; no query or fragment")
    ap.add_argument("--path", action="append", help="Explicitly permitted origin-relative path, repeat max 3; default / or URL path")
    ap.add_argument("--out", required=True, help="Directory for JSON report and public-page viewport screenshots")
    ap.add_argument("--remote-public", action="store_true", help="Explicit public HTTPS browsing authorization; NOT for authenticated/private pages")
    ap.add_argument("--chrome-path", help="Optional existing trusted Chromium executable; otherwise use Playwright-managed Chromium")
    ns=ap.parse_args(argv)
    try:
        _, default_path=check_target(ns.url,ns.remote_public)
        report=run_audit(ns.url, ns.path or [default_path], Path(ns.out).resolve(),ns.remote_public,ns.chrome_path)
        print(json.dumps({"status":report["status"],"pages":len(report["pages"]),"observed":sum(p['result']=='OBSERVED' for p in report['pages']),"report":str(Path(ns.out).resolve()/"browser-ux-report.json")},ensure_ascii=False))
        return 0 if report["status"] == "COMPLETE" else 2
    except (ValueError, ImportError, OSError) as exc:
        print("BLOCKED_BROWSER_AUDIT: " + str(exc),file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
