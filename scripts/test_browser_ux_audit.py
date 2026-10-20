#!/usr/bin/env python3
"""Read-only policy tests + optional real Chromium local loopback smoke test."""
from __future__ import annotations
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import shutil
import tempfile
import threading
import unittest
from browser_ux_audit import (check_target, normalized_path, origin_of, DOM_READ_JS,
                              policy_for_request, make_findings, run_audit)


class BrowserPolicyTests(unittest.TestCase):
    def test_allowed_methods_origin(self):
        o = 'http://127.0.0.1:8080'
        self.assertEqual(policy_for_request(o+'/','GET',o),'ALLOW')
        self.assertEqual(policy_for_request(o+'/','POST',o),'BLOCK_WRITE_METHOD')
        self.assertEqual(policy_for_request(o+'/','DELETE',o),'BLOCK_WRITE_METHOD')
        self.assertEqual(policy_for_request('http://127.0.0.1:9000/','GET',o),'BLOCK_CROSS_ORIGIN')
        self.assertEqual(policy_for_request('file:///etc/passwd','GET',o),'BLOCK_NON_HTTP')
    def test_remote_denied_by_default(self):
        with self.assertRaisesRegex(ValueError,'remote site requires'):
            check_target('https://example.com/',False)
        with self.assertRaisesRegex(ValueError,'https'):
            check_target('http://example.com/',True)
    def test_private_url_and_credentials_denied(self):
        with self.assertRaises(ValueError): origin_of('http://name:pass@127.0.0.1:8000')
        with self.assertRaises(ValueError): check_target('http://10.0.0.2/',True)
    def test_paths_are_bounded(self):
        self.assertEqual(normalized_path('/kontakt'), '/kontakt')
        for p in ['//evil.test','/../admin','/%2e%2e/admin','/contact?a=1','/a#b','/\\admin']:
            with self.subTest(p=p), self.assertRaises(ValueError): normalized_path(p)
    def test_heuristic_findings_not_conversion_claims(self):
        issues=make_findings({'headings':[],'actions':[],'forms':[], 'overflow_x_px':55},'mobile')
        self.assertTrue({'HEADING_MISSING','HORIZONTAL_OVERFLOW','NO_VISIBLE_CTA_CANDIDATE'}.issubset({i['id'] for i in issues}))
        self.assertFalse(any('uplift' in i['observation'].lower() for i in issues))


class SyntheticBrowserRenderTests(unittest.TestCase):
    def test_dom_and_viewport_without_network(self):
        chrome = shutil.which('chromium') or shutil.which('google-chrome')
        if not chrome: self.skipTest('no system browser for synthetic smoke')
        from playwright.sync_api import sync_playwright
        with sync_playwright() as playwright:
            browser=playwright.chromium.launch(headless=True,executable_path=chrome)
            try:
                page=browser.new_page(viewport={'width':390,'height':844})
                page.set_content('<h1>Beratung jetzt buchen</h1><a href="/kontakt">Termin buchen</a><form><input type="email"></form>')
                data=page.evaluate(DOM_READ_JS)
                self.assertEqual(data['headings'][0]['text'],'Beratung jetzt buchen')
                self.assertTrue(any(a['rect']['inViewport'] for a in data['actions']))
                self.assertEqual(data['forms'][0]['fields'][0]['labelled'],False)
                self.assertTrue(any(x['id']=='FORM_LABEL_REVIEW' for x in make_findings(data,'mobile')))
                with tempfile.TemporaryDirectory() as folder:
                    screenshot=Path(folder)/'synthetic.png'
                    page.screenshot(path=str(screenshot))
                    self.assertGreater(screenshot.stat().st_size,1000)
                page.close()
            finally:
                browser.close()


class SmokeServer(BaseHTTPRequestHandler):
    visits=[]
    posts=[]
    def do_GET(self):
        self.__class__.visits.append(self.path)
        if self.path=='/redirect':
            self.send_response(302)
            self.send_header('Location','http://127.0.0.1:1/private')
            self.end_headers()
            return
        html='''<!doctype html><html lang="de"><head><title>Local conversion test</title>
        <meta name="viewport" content="width=device-width,initial-scale=1"></head>
        <body><main><h1>Testberatung fuer Selbststaendige</h1>
        <p>Pruefen Sie den passenden Termin</p><a href="/kontakt">Termin buchen</a>
        <form action="/submit" method="post"><input id="mail" type="email" required>
        <button type="submit">Anfrage senden</button></form>
        </main><script>fetch('/writing-api',{method:'POST',body:'blocked'}).catch(()=>{});
        new WebSocket('ws://127.0.0.1:1/blocked');</script></body></html>'''
        data=html.encode()
        self.send_response(200)
        self.send_header('Content-Type','text/html; charset=utf-8')
        self.send_header('Content-Length',str(len(data)))
        self.end_headers()
        self.wfile.write(data)
    def do_POST(self):
        self.__class__.posts.append(self.path)
        self.send_response(200);self.end_headers()
    def log_message(self,fmt,*args): pass


class BrowserIntegrationSmoke(unittest.TestCase):
    def test_bounded_readonly_smoke(self):
        chrome = shutil.which('chromium') or shutil.which('google-chrome')
        if not chrome:
            self.skipTest('system Chromium unavailable; manual smoke needed')
        try:
            import playwright  # noqa: F401
        except ImportError:
            self.skipTest('playwright package unavailable')
        SmokeServer.visits=[]; SmokeServer.posts=[]
        server=ThreadingHTTPServer(('127.0.0.1',0),SmokeServer)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            with tempfile.TemporaryDirectory() as temp:
                url=f'http://127.0.0.1:{server.server_port}'
                report=run_audit(url,['/'],Path(temp),False,chrome)
                if (report["status"] == "NOT_TESTED" and
                    all(any("ERR_BLOCKED_BY_ADMINISTRATOR" in error for error in page["errors"]) for page in report["pages"])):
                    self.skipTest("environment administrator blocks Chromium localhost navigation")
                self.assertEqual(report['status'],'COMPLETE',report)
                self.assertEqual(len(report['pages']),2)
                self.assertEqual(SmokeServer.posts,[],'unsafe POST reached server')
                self.assertGreaterEqual(report['blocked_requests'].get('BLOCK_WRITE_METHOD',0),2)
                self.assertEqual(report['pages'][0]['data']['forms'][0]['fields'][0]['labelled'],False)
                self.assertTrue((Path(temp)/'browser-ux-report.json').exists())
                self.assertTrue((Path(temp)/'mobile-1.png').exists())
                self.assertIn('form submission',report['not_tested'])
        finally:
            server.shutdown(); server.server_close(); thread.join(timeout=2)


if __name__=='__main__':
    unittest.main(verbosity=2)
