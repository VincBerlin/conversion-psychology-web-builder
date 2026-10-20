#!/usr/bin/env python3
"""Deterministic browser policy oracle + mutant rejection test, no network.

An unconditional ALLOW mutation must fail the policy oracle and thus packaging.
"""
from __future__ import annotations
import ast
from pathlib import Path
import sys
import unittest
import browser_ux_audit


def oracle(policy):
    origin='http://127.0.0.1:8080'
    cases=[
        (origin+'/','GET','ALLOW'),
        (origin+'/','HEAD','ALLOW'),
        (origin+'/','POST','BLOCK_WRITE_METHOD'),
        (origin+'/','PUT','BLOCK_WRITE_METHOD'),
        (origin+'/','PATCH','BLOCK_WRITE_METHOD'),
        (origin+'/','DELETE','BLOCK_WRITE_METHOD'),
        ('http://127.0.0.1:8081/','GET','BLOCK_CROSS_ORIGIN'),
        ('https://example.org/','GET','BLOCK_CROSS_ORIGIN'),
        ('file:///etc/passwd','GET','BLOCK_NON_HTTP'),
        ('javascript:alert(1)','GET','BLOCK_NON_HTTP'),
    ]
    return [(url,method,expected,policy(url,method,origin)) for url,method,expected in cases if policy(url,method,origin)!=expected]


def mutant_policy():
    """Produce test-only mutation without modifying the actual skill file."""
    path=Path(browser_ux_audit.__file__)
    tree=ast.parse(path.read_text(encoding='utf-8'))
    fn=next(n for n in tree.body if isinstance(n,(ast.FunctionDef, ast.AsyncFunctionDef)) and n.name=='policy_for_request')
    idx=1 if isinstance(fn.body[0],ast.Expr) and isinstance(fn.body[0].value,ast.Constant) and isinstance(fn.body[0].value.value,str) else 0
    fn.body.insert(idx,ast.Return(value=ast.Constant(value='ALLOW')))
    ast.fix_missing_locations(tree)
    module={'__name__':'browser_policy_mutant'}
    exec(compile(tree,str(path),'exec'),module)
    return module['policy_for_request']


class GateMutationTests(unittest.TestCase):
    def test_real_policy_blocks_writes_cross_origin_and_non_http(self):
        self.assertEqual(oracle(browser_ux_audit.policy_for_request), [],'unsafe actual network policy passed')
    def test_oracle_rejects_unconditional_allow_mutation(self):
        failures=oracle(mutant_policy())
        self.assertGreaterEqual(len(failures),4,'mutation oracle did not catch policy regression')
        self.assertTrue(any(x[1]=='POST' for x in failures))

if __name__=='__main__':unittest.main(verbosity=2)
