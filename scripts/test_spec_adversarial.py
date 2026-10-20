#!/usr/bin/env python3
"""Negative and publication-gate tests; no network, no external mutations."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from validate_design_spec import check_spec,check_publication,safe_cta_target

ROOT=Path(__file__).resolve().parent.parent
BASE=json.loads((ROOT/'evals/fixtures/013-pass-precision-v2-minimal.json').read_text())
BASE.pop('_expected',None)

class SpecAdversarialTests(unittest.TestCase):
    def test_valid_v2_baseline(self):self.assertEqual(check_spec(copy.deepcopy(BASE)),[])
    def test_dangerous_ctas(self):
        for target in ['javascript:alert(1)','//evil.com','https://evil.com','/%2e%2e/admin','/\\evil','data:text/html,hi','/kontakt\nHost:evil','#','mailto:notanaddress']:
            with self.subTest(target=target):self.assertFalse(safe_cta_target(target))
    def test_empty_and_wrong_types_are_controlled_errors(self):
        for value in [None,[],{},1,True,False,'','x']:
            for field in ['mode','decision','evidence_level','patterns','guardrail_metrics','primary_cta','claims','baseline_status','tracking_status','decision_type','interventions']:
                x=copy.deepcopy(BASE);x[field]=value
                with self.subTest(field=field,value=repr(value)):
                    result=check_spec(x)
                    self.assertIsInstance(result,list)
                    if not (field in {'patterns','claims'} and value==[]):
                        self.assertTrue(result)
    def test_audit_never_authorizes_build(self):
        for mode in ['AUDIT_ONLY','PLAN_ONLY']:
            spec=copy.deepcopy(BASE);spec['mode']=mode
            self.assertIn('cannot authorize build', ' '.join(check_spec(spec)))
    def test_legacy_no_publication(self):
        spec=copy.deepcopy(BASE);spec.pop('strategy_version')
        self.assertTrue(check_publication(spec,Path('.')))
    def test_claim_file_references_are_not_self_asserting(self):
        spec=copy.deepcopy(BASE)
        spec['claims']=[{'text':'Proof claim','verification_status':'verified','source':'test','publish':True,'evidence_ref':'proof.txt','approval_ref':'approval.txt'}]
        self.assertEqual(check_spec(spec),[])
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            self.assertTrue(check_publication(spec,root))
            for file in ('proof.txt','approval.txt','observations.txt'):(root/file).write_text('fixture only, no real proof')
            spec['observation_ref']='observations.txt'
            self.assertEqual(check_publication(spec,root),[])
    def test_approval_refs_must_stay_in_scope(self):
        x=copy.deepcopy(BASE);x['claims']=[{'text':'claim','source':'s','verification_status':'verified','evidence_ref':'../etc/passwd','approval_ref':'foo'}]
        with tempfile.TemporaryDirectory() as d:
            self.assertTrue(check_publication(x,Path(d)))

if __name__=='__main__':unittest.main(verbosity=2)
