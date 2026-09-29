#!/usr/bin/env python3
"""Run real bounded portable evidence in an owned isolated snapshot, never ordinary checkout."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from fixturelib import execute,git,save,sha
p=argparse.ArgumentParser(); p.add_argument('fixture_root',type=Path); a=p.parse_args(); root=a.fixture_root.resolve()
row=next(row for row in json.loads((root/'manifest.json').read_text()) if row['id']=='bounded_rename'); repo=Path(row['repository']); target=row['variants']['clean']
if git(repo,'rev-parse','HEAD')!=target or git(repo,'status','--porcelain'): raise SystemExit('Fixture checkout is not clean at expected exact target')
evidence=root/'evidence/bounded-rename'
if evidence.exists(): raise SystemExit('Refusing to overwrite existing evidence')
evidence.mkdir(parents=True); scratch=Path(tempfile.mkdtemp(prefix='ios-ultrareview-bounded-',dir='/private/tmp')); results=[]
record={'kind':'Actually executed local SwiftPM evidence; not synthetic CI or iOS runtime proof','target':target,'repository':str(repo),'destination':'arm64-apple-macosx host; pure cross-platform library','swift_version':subprocess.check_output(['swift','--version'],stderr=subprocess.STDOUT,text=True).strip(),'limits':'This case has no Apple adapters, signing, lifecycle, concurrency or device-specific artifacts/behavior. Execution occurs in an owned archived snapshot and caches; ordinary checkout is preserved.'}
try:
 material=scratch/'snapshot'; material.mkdir(); archive=scratch/'source.tar'
 with archive.open('wb') as stream: subprocess.run(['git','-C',str(repo),'archive',target],stdout=stream,check=True)
 record['source_archive_sha256']=sha(archive)
 with tarfile.open(archive) as package:
  for member in package.getmembers():
   if member.issym() or member.islnk() or not (material/member.name).resolve().is_relative_to(material): raise SystemExit('Unsafe snapshot member')
  package.extractall(material)
 env=dict(os.environ); env['CLANG_MODULE_CACHE_PATH']=str(scratch/'clang-cache')
 for action in ['build','test']:
  command=['swift',action,'--build-system','native','--scratch-path',str(scratch/'build'),'--disable-sandbox','--cache-path',str(scratch/'cache'),'--config-path',str(scratch/'config'),'--security-path',str(scratch/'security')]
  results.append(execute(command,material,evidence/f'swift-{action}.log',env)); print(f'{action}: exit {results[-1]["exit_code"]}',flush=True)
  if results[-1]['exit_code']: break
 record['results']=results; record['repository_status_after']=git(repo,'status','--porcelain')
finally: shutil.rmtree(scratch)
save(evidence/'record.json',record)
if len(results)!=2 or any(r['exit_code'] for r in results) or record['repository_status_after']: raise SystemExit(1)
input_map=json.loads((root/'evaluator/input-map.json').read_text()); review_input=Path(next(item['input'] for item in input_map if item['id']=='bounded_rename'))
with review_input.open('a') as stream: stream.write(f'\nSupplied actually executed local exact-head build/test evidence: `{evidence}/record.json`. Read that record and its logs. Host portable-library evidence only; no CI, simulator or device claim.\n')
