#!/usr/bin/env python3
"""Execute visible tests or hidden adjudication after verified prediction freezing."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from fixturelib import execute,git,save,sha,utc
p=argparse.ArgumentParser(); p.add_argument('suite',type=Path); p.add_argument('--input-number',type=int,required=True)
g=p.add_mutually_exclusive_group(required=True); g.add_argument('--public',action='store_true'); g.add_argument('--hidden',action='store_true')
p.add_argument('--freeze',type=Path); a=p.parse_args(); root=a.suite.resolve()
entry=json.loads((root/'evaluator/input-map.json').read_text())[a.input_number-1]
row=next(r for r in json.loads((root/'manifest.json').read_text()) if r['id']==entry['id']); repo=Path(row['repository']); target=entry['head']
freeze=None
if a.hidden:
 if not a.freeze: raise SystemExit('Hidden evaluator requires --freeze record.json made before exposure')
 freeze=json.loads(a.freeze.read_text()); folder=a.freeze.parent
 if freeze['head']!=target or freeze['base']!=row['base'] or sha(Path(entry['input']))!=freeze['artifacts']['input.md']: raise SystemExit('Frozen target/input does not match evaluator case')
 for name,digest in freeze['artifacts'].items():
  if sha(folder/name)!=digest: raise SystemExit(f'Frozen artifact modified: {name}')
 if not freeze.get('no_hidden_access_before_freeze'): raise SystemExit('Independent discovery requires no pre-freeze hidden access attestation')
 if not freeze['fresh_context_per_case']: raise SystemExit('Independent discovery requires a fresh context per case')
 git(repo,'cat-file','-e',target+'^{commit}')
kind='hidden' if a.hidden else 'public'; evidence=root/'evaluator'/'runs'/f'input-{a.input_number:02d}-{kind}'
if evidence.exists(): raise SystemExit('Refusing to overwrite an evaluator run; generate a fresh suite or archive the old run')
evidence.mkdir(parents=True)
record={'input':entry['input'],'target':target,'kind':kind,'started_utc':utc(),'freeze_record':str(a.freeze) if a.freeze else None,'freeze_record_sha256':sha(a.freeze) if a.freeze else None,'limits':'Local portable checks only; no production, iOS runtime, lock-state or real paired delivery validation.'}
if a.hidden and row['evaluator_kind']=='static_platform_contract':
 source=git(repo,'show',target+':Sources/ReviewFixture/CredentialPolicy.swift')
 adapter=git(repo,'show',target+':PlatformIntegration/RefreshTokenStore.swift')
 protected_after_first_unlock=('= .afterFirstUnlockDeviceOnly' in source and 'kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly' in adapter)
 record.update({'adjudication_kind':'Static fixture-specific policy/adapter contract audit, not independent runtime proof','product_outcome_satisfied':protected_after_first_unlock,'runtime_test_executed':False,'source':source,'adapter':adapter})
else:
 scratch=Path(tempfile.mkdtemp(prefix='ios-review-eval-',dir='/private/tmp')); material=scratch/'snapshot'; material.mkdir()
 try:
  archive=scratch/'snapshot.tar'
  with archive.open('wb') as stream: subprocess.run(['git','-C',str(repo),'archive',target],stdout=stream,check=True)
  with tarfile.open(archive) as package:
   for member in package.getmembers():
    if member.issym() or member.islnk() or not (material/member.name).resolve().is_relative_to(material): raise SystemExit('Unsafe archive member')
   package.extractall(material)
  if a.hidden: shutil.copyfile(row['hidden_test'],material/'Tests/ReviewFixtureTests/HiddenOutcomeTests.swift')
  env=dict(os.environ); env['CLANG_MODULE_CACHE_PATH']=str(scratch/'clang-cache')
  command=['swift','test','--build-system','native','--scratch-path',str(scratch/'build'),'--disable-sandbox','--cache-path',str(scratch/'cache'),'--config-path',str(scratch/'config'),'--security-path',str(scratch/'security')]
  result=execute(command,material,evidence/'swift-test.log',env)
  output=(evidence/'swift-test.log').read_text()
  record.update({
   'results':[result],
   'tests_reached':"Executed " in output,
   'assertion_failure':"XCTAssert" in output and "failed" in output,
   'outcome_test_failure':bool(re.search(r"(?m)^Test Case .+HiddenOutcomeTests.+ failed [(]",output)),
   'swift_version':subprocess.check_output(['swift','--version'],stderr=subprocess.STDOUT,text=True).strip(),
   'hidden_test_sha256':sha(row['hidden_test']) if a.hidden else None,
  })
 finally: shutil.rmtree(scratch)
record['completed_utc']=utc(); save(evidence/'record.json',record)
print(json.dumps(record,indent=2))
if a.public and (record['results'][0]['exit_code'] or not record['tests_reached']): raise SystemExit(1)
if a.hidden and row['evaluator_kind']=='outcome_test' and not record['tests_reached']: raise SystemExit('Compilation/tool failure is not a seeded test outcome')
