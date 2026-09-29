#!/usr/bin/env python3
"""Run real host/app evidence and explicit local state events; never fabricate CI."""
import argparse
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from fixturelib import execute,execute_json,git,prompt,save,sha,tree_hash,utc
p=argparse.ArgumentParser(); p.add_argument('suite',type=Path)
p.add_argument('action',choices=['focused','app-baseline','optional','xcode-clean','xcode-defect','advance-head','inspect-acquisition','inject-mutation','xcode-adjudicate'])
p.add_argument('--input',choices=['X1','X2'],help='Frozen Xcode case for hidden static adjudication')
p.add_argument('--destination',help='Actual installed simulator: platform=iOS Simulator,id=UUID')
p.add_argument('--freeze',type=Path,help='Frozen A3 review before optional evaluator access')
p.add_argument('--optional-item',help='Previously published stable item, e.g. E1')
p.add_argument('--pass-condition',help='Exact cancellation outcome condition quoted from the frozen review')
p.add_argument('--adjudicated-cancellation-item',action='store_true',help='Evaluator attests this selected frozen item/condition matches the supplied cancellation test outcome')
a=p.parse_args(); root=a.suite.resolve(); rows=json.loads((root/'manifest.json').read_text()); onboarding=rows[0]; xcode=rows[1]; acq=rows[2]
evidence=(root/'evidence'/('X2' if a.action=='xcode-clean' else 'X1')) if a.action in ['xcode-clean','xcode-defect'] else root/'evaluator'/'runs'/(a.action+('-'+a.input if a.input else ''))
if evidence.exists(): raise SystemExit('Refusing to overwrite a prior run; archive it or use a fresh generated suite')
record={'action':a.action,'started_utc':utc(),'limits':'Actually executed local commands only. Simulator results are not physical-device/permission/background evidence. Local provider fixtures do not test hosted network/authentication APIs.'}
if a.action=='advance-head':
 git(acq['provider'],'update-ref','refs/heads/review-target',acq['advanced_head'])
 save(acq['current'],{'base':acq['base'],'head':acq['advanced_head'],'repository':acq['provider']})
 record.update({'previous_head':acq['head'],'current_head':acq['advanced_head'],'provider_ref':git(acq['provider'],'rev-parse','refs/heads/review-target')})
elif a.action=='inspect-acquisition':
 owner=json.loads((root/'evaluator/ownership.json').read_text()); states={}
 for key,path in owner.items():
  r=Path(path); states[key]={'path':path,'exists':r.exists()}
  if r.exists(): states[key].update({'head':git(r,'rev-parse','HEAD'),'status':git(r,'status','--porcelain')})
 record['states']=states; record['current_provider']=json.loads(Path(acq['current']).read_text())
elif a.action=='inject-mutation':
 # Test fixture only: exact manifest path and SHA, no reset/clean/delete of unknown paths.
 repo=Path(acq['mutation_repository'])
 if git(repo,'rev-parse','HEAD')!=acq['mutation_head'] or git(repo,'status','--porcelain'): raise SystemExit('Mutation fixture must be untouched at exact generated head')
 for name in ['known-output','unexpected.txt']:
  if (repo/name).exists(): raise SystemExit('Mutation path already exists')
 (repo/'README.md').write_text('# Regenerated validation notes\n'); (repo/'known-output').mkdir(); (repo/'known-output/report.txt').write_text('Evaluator-injected known output.\n'); (repo/'unexpected.txt').write_text('Unexpected content must be retained.\n')
 record.update({'kind':'Explicit evaluator state-event injection; no build command claimed','repository':str(repo),'head':acq['mutation_head'],'status_after':git(repo,'status','--porcelain')})
elif a.action=='xcode-adjudicate':
 if not a.freeze or not a.input: raise SystemExit('Hidden configuration audit requires frozen review and X1/X2')
 target=xcode['variants']['defect' if a.input=='X1' else 'clean']; frozen=json.loads(a.freeze.read_text()); fdir=a.freeze.parent
 if frozen['head']!=target or frozen['base']!=xcode['base']: raise SystemExit('Frozen Xcode target does not match')
 if not frozen.get('no_hidden_access_before_freeze') or not frozen['fresh_context_per_case']: raise SystemExit('Independent adjudication requires fresh context and no pre-freeze hidden access')
 if frozen['artifacts']['input.md']!=sha(root/'inputs'/f'{a.input}.md'): raise SystemExit('Frozen input mismatch')
 for name,digest in frozen['artifacts'].items():
  if sha(fdir/name)!=digest: raise SystemExit('Frozen artifact modified')
 scratch=Path(tempfile.mkdtemp(prefix='ios-config-audit-',dir='/private/tmp'))
 try:
  archive=scratch/'source.tar'; material=scratch/'snapshot'; material.mkdir()
  with archive.open('wb') as stream: subprocess.run(['git','-C',xcode['repository'],'archive',target],stdout=stream,check=True)
  with tarfile.open(archive) as package:
   for member in package.getmembers():
    if member.issym() or member.islnk() or not (material/member.name).resolve().is_relative_to(material): raise SystemExit('Unsafe archive')
   package.extractall(material)
  settings=execute_json(['xcodebuild','-project','FixtureApp.xcodeproj','-scheme','FixtureApp','-configuration','Debug','-sdk','iphonesimulator','-derivedDataPath',str(scratch/'DerivedData'),'-showBuildSettings','-json'],material,evidence/'build-settings.json')
  if settings['exit_code']: raise SystemExit('Build-setting command failed; no static product adjudication')
  try: effective=json.loads((evidence/'build-settings.json').read_text())
  except json.JSONDecodeError as error:
   record.update({'results':[settings],'infrastructure_error':str(error)}); save(evidence/'record.json',record); raise SystemExit('Xcode structured settings were not parseable; no adjudication')
  app=next(r['buildSettings'] for r in effective if r['target']=='FixtureApp')
  record.update({'head':target,'base':xcode['base'],'freeze_record':str(a.freeze),'freeze_record_sha256':sha(a.freeze),'results':[settings],'effective_app_settings':{key:app.get(key) for key in ['IPHONEOS_DEPLOYMENT_TARGET','TARGETED_DEVICE_FAMILY','SUPPORTED_PLATFORMS']},'static_release_contract_satisfied':app.get('IPHONEOS_DEPLOYMENT_TARGET')=='17.0' and app.get('TARGETED_DEVICE_FAMILY')=='1,2','adjudication_kind':'Actual effective-build-setting check of static supported-release contract; no old-runtime/iPad execution claim'})
 finally: shutil.rmtree(scratch)
else:
 row=xcode if a.action.startswith('xcode-') else onboarding
 target=row['variants']['clean' if a.action=='xcode-clean' else 'defect'] if a.action.startswith('xcode-') else row['A2']
 repo=Path(row['repository']); git(repo,'cat-file','-e',target+'^{commit}')
 record.update({'base':row['base'],'head':target,'repository':str(repo),'xcode_version':subprocess.check_output(['xcodebuild','-version'],text=True).strip(),'swift_version':subprocess.check_output(['swift','--version'],stderr=subprocess.STDOUT,text=True).strip(),'repository_status_before':git(repo,'status','--porcelain')})
 if a.action=='optional':
  if not a.freeze or not a.optional_item or not a.pass_condition or not a.adjudicated_cancellation_item: raise SystemExit('Optional evidence requires frozen review, stable item, exact condition and evaluator cancellation-equivalence attestation')
  frozen=json.loads(a.freeze.read_text()); fdir=a.freeze.parent
  if frozen['head']!=target or frozen['base']!=row['base']: raise SystemExit('Frozen review target does not match')
  for name,digest in frozen['artifacts'].items():
   if sha(fdir/name)!=digest: raise SystemExit('Frozen artifact changed')
  review=(fdir/'review.md').read_text()
  if not re.fullmatch(r'E[1-9][0-9]*',a.optional_item) or not re.search(r'(?<![A-Za-z0-9_])'+re.escape(a.optional_item)+r'(?![A-Za-z0-9_])',review): raise SystemExit('Exact optional ID was not present in frozen review')
  if a.pass_condition not in review: raise SystemExit('Quoted pass condition was not present in frozen review')
  condition=a.pass_condition.casefold()
  if 'cancel' not in condition or not any(term in condition for term in ['complet','dismiss']): raise SystemExit('Named condition does not explicitly describe the cancellation completion outcome')
  baseline=root/'evaluator/runs/app-baseline/record.json'
  if not baseline.exists(): raise SystemExit('Qualifying A3 app baseline has not actually executed')
  data=json.loads(baseline.read_text())
  if not data.get('qualifies') or data.get('head')!=target or len(data.get('results',[]))!=2: raise SystemExit('A3 baseline did not qualify on this head')
  for result in data['results']:
   if result['exit_code'] or sha(result['log'])!=result['log_sha256']: raise SystemExit('A3 executed evidence is failed or modified')
  if '** TEST EXECUTE SUCCEEDED **' not in Path(data['results'][-1]['log']).read_text(): raise SystemExit('A3 hosted tests did not execute successfully')
  record.update({'frozen_review':str(a.freeze),'frozen_review_sha256':sha(a.freeze),'stable_optional_item':a.optional_item,'frozen_pass_condition':a.pass_condition,'evaluator_attested_cancellation_equivalence':True,'semantic_adjudication_limit':'The evaluator must judge that the quoted condition belongs to the selected stable item; substring checks do not independently prove semantic equivalence.','baseline_record':str(baseline),'baseline_record_sha256':sha(baseline)})
 scratch=Path(tempfile.mkdtemp(prefix='ios-stateful-eval-',dir='/private/tmp'))
 try:
  material=scratch/'snapshot'; material.mkdir(); archive=scratch/'source.tar'
  with archive.open('wb') as stream: subprocess.run(['git','-C',str(repo),'archive',target],stdout=stream,check=True)
  record['source_archive_sha256']=sha(archive)
  with tarfile.open(archive) as package:
   for member in package.getmembers():
    if member.issym() or member.islnk() or not (material/member.name).resolve().is_relative_to(material): raise SystemExit('Unsafe generated archive')
   package.extractall(material)
  env=dict(os.environ); env['CLANG_MODULE_CACHE_PATH']=str(scratch/'clang-cache')
  results=[]
  if a.action in ['focused','optional']:
   if a.action=='optional':
    extra=(root/onboarding['cancellation_test']).read_text()
    with (material/'Tests/ReviewFixtureTests/ProfileSetupTests.swift').open('a') as stream: stream.write(extra)
    record['supplemental_test_sha256']=sha(root/onboarding['cancellation_test']); record['supplemental_test_scope']='Additive evaluator tests; application source is the exact target; no reviewed source changes.'
   for action in ['build','test']:
    cmd=['swift',action,'--build-system','native','--scratch-path',str(scratch/'swift-build'),'--disable-sandbox','--cache-path',str(scratch/'cache'),'--config-path',str(scratch/'config'),'--security-path',str(scratch/'security')]
    results.append(execute(cmd,material,evidence/f'swift-{action}.log',env))
    if results[-1]['exit_code']: break
   qualifies=len(results)==2 and all(r['exit_code']==0 for r in results) and 'Executed ' in (evidence/'swift-test.log').read_text()
  else:
   if not a.destination or 'id=' not in a.destination: raise SystemExit('Use an actual installed simulator destination including its UUID')
   common=['xcodebuild','-project','FixtureApp.xcodeproj','-scheme','FixtureApp','-configuration','Debug','-destination',a.destination,'-derivedDataPath',str(scratch/'DerivedData'),'CODE_SIGNING_ALLOWED=NO']
   for action in ['build-for-testing','test-without-building']:
    cmd=common+[action,'-resultBundlePath',str(evidence/f'{action}.xcresult')]
    results.append(execute(cmd,material,evidence/f'xcode-{action}.log',env))
    if results[-1]['exit_code']: break
   qualifies=len(results)==2 and all(r['exit_code']==0 for r in results) and '** TEST EXECUTE SUCCEEDED **' in (evidence/'xcode-test-without-building.log').read_text()
  record.update({'results':results,'qualifies':qualifies,'repository_status_after':git(repo,'status','--porcelain')})
 finally: shutil.rmtree(scratch)
 if record['repository_status_before']!=record['repository_status_after']: record['qualifies']=False
record['completed_utc']=utc(); save(evidence/'record.json',record); print(json.dumps(record,indent=2))
if a.action in ['focused','app-baseline','optional','xcode-clean','xcode-defect'] and not record['qualifies']: raise SystemExit(1)
if a.action=='app-baseline':
 path=root/'inputs/A3.md'; path.write_text(prompt(onboarding['repository'],onboarding['base'],onboarding['A3'],f'Supplied actually executed exact-head app-scheme build/test evidence: `{evidence}/record.json` and its named logs. Read only this evidence, not sibling evaluator resources. For re-review, use the immediately preceding frozen review supplied by the evaluator. No supplemental interruption test is supplied.'))
if a.action=='optional':
 path=root/'inputs/A4.md'; path.write_text(prompt(onboarding['repository'],onboarding['base'],onboarding['A4'],f'Supplied actually executed exact-head app baseline: `{root}/evaluator/runs/app-baseline/record.json`. Supplemental focused outcome evidence: `{evidence}/record.json` and its logs, for prior item `{a.optional_item}`. Read only these records/logs and the immediately preceding frozen review supplied by the evaluator; no sibling oracle access.'))

if a.action in ['xcode-clean','xcode-defect']:
 name='X2' if a.action=='xcode-clean' else 'X1'
 public=root/'evidence'/name; public.mkdir(parents=True,exist_ok=True)
 # Actual results only; no expected labels or evaluator conclusions in reviewer artifacts.
 supplied={key:value for key,value in record.items() if key not in ['action','qualifies']}
 save(root/'evaluator/runs'/(a.action+'-neutral')/'record.json',record)
 save(public/'record.json',supplied)
 with (root/'inputs'/f'{name}.md').open('a') as stream: stream.write(f'\nSupplied actually executed exact-head app-scheme build/test evidence: `{public}/record.json` and its named logs. This covers the current iPhone simulator; no old-iOS/iPad runtime result or CI claim is supplied.\n')
