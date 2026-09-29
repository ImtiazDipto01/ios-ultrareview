#!/usr/bin/env python3
"""Freeze a reviewer prediction before hidden evaluator access; no model API calls."""
import argparse
import json
import re
from pathlib import Path
import sys
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))
from fixturelib import fresh,save,sha,tree_hash,utc
p=argparse.ArgumentParser()
p.add_argument('--input',type=Path,required=True); p.add_argument('--review',type=Path,required=True)
p.add_argument('--skill',type=Path,required=True); p.add_argument('--head',required=True); p.add_argument('--base',required=True)
p.add_argument('--model',required=True,help='Actual provider/model identifier, or explicit unknown/session-inherited when unavailable; never infer it')
p.add_argument('--settings-json',type=Path,required=True); p.add_argument('--tools-json',type=Path,required=True)
p.add_argument('--command-log',type=Path); p.add_argument('--elapsed-seconds',type=float); p.add_argument('--tokens',type=int)
p.add_argument('--public-benchmark',action='store_true',help='Require a known model, recorded settings and hash-bound host/provider provenance before freezing')
p.add_argument('--provenance-json',type=Path,help='Recorded metadata envelope; see docs/evaluation.md')
p.add_argument('--no-hidden-access',action='store_true',help='Attest no hidden evaluator/source/results access before freezing')
p.add_argument('--fresh-context',action='store_true',help='Attest a new context was used for this one case')
p.add_argument('--output',type=Path,required=True)
a=p.parse_args()
for source in [a.input,a.review,a.settings_json,a.tools_json]:
 if not source.is_file(): raise SystemExit(f'Missing required artifact: {source}')
if a.command_log and not a.command_log.is_file(): raise SystemExit(f'Missing command log: {a.command_log}')
if not a.skill.is_dir() or not (a.skill/'SKILL.md').is_file(): raise SystemExit('Skill directory must contain SKILL.md')
input_text=a.input.read_text()
for label,provided in [('Base',a.base),('Head',a.head)]:
 field=re.search(r'(?m)^'+label+r':\s*([^\n]+)$',input_text)
 if field:
  stated=field.group(1).strip().strip('`').strip()
  if not re.fullmatch(r'(?:[0-9a-fA-F]{40}|[0-9a-fA-F]{64})',stated): raise SystemExit(f'Structured {label} field must be an immutable full Git SHA')
  if stated.casefold()!=provided.casefold(): raise SystemExit(f'Provided {label} SHA does not match the structured input')
settings=json.loads(a.settings_json.read_text()); tool_metadata=json.loads(a.tools_json.read_text())
if not isinstance(settings,dict) or not isinstance(tool_metadata,dict): raise SystemExit('Settings/tools metadata must be JSON objects')
if a.tokens is not None and a.tokens<0: raise SystemExit('Token count cannot be negative')
if a.elapsed_seconds is not None and (a.elapsed_seconds<0 or not __import__('math').isfinite(a.elapsed_seconds)): raise SystemExit('Elapsed seconds must be finite and nonnegative')
provenance=None; provenance_source=None
if a.public_benchmark:
 if not a.model.strip() or a.model.strip().casefold() in {'unknown','null','none','session-inherited','inherited','unavailable','n/a'}:
  raise SystemExit('Public benchmark requires a known actual model identifier')
 if not settings or not any(v is not None and str(v).strip().casefold() not in {'','unknown','null','none','unavailable','n/a'} for v in settings.values()):
  raise SystemExit('Public benchmark requires at least one recorded model setting; disclose other unknown settings')
 if not a.provenance_json or not a.provenance_json.is_file(): raise SystemExit('Public benchmark requires --provenance-json')
 provenance=json.loads(a.provenance_json.read_text())
 if not isinstance(provenance,dict): raise SystemExit('Provenance must be a JSON object')
 if provenance.get('model')!=a.model or provenance.get('settings')!=settings: raise SystemExit('Provenance model/settings do not match supplied metadata')
 source=provenance.get('source',{})
 if not isinstance(source,dict) or source.get('kind') not in {'host-recorded','provider-recorded'} or not str(source.get('label','')).strip():
  raise SystemExit('Provenance needs a named host-recorded or provider-recorded source')
 artifact=source.get('artifact'); digest=source.get('sha256')
 if not isinstance(artifact,str) or not isinstance(digest,str) or not re.fullmatch(r'[a-f0-9]{64}',digest): raise SystemExit('Provenance source requires artifact and SHA-256')
 provenance_source=(a.provenance_json.parent/artifact).resolve()
 if not provenance_source.is_file() or sha(provenance_source)!=digest: raise SystemExit('Provenance source missing or hash mismatch')
 if a.tokens is not None:
  usage=provenance.get('usage',{})
  if not isinstance(usage,dict) or usage.get('total_tokens')!=a.tokens or not isinstance(usage.get('scope'),str) or not usage['scope'].strip():
   raise SystemExit('Measured tokens need matching provenance usage and an explicit scope')
elif a.provenance_json:
 raise SystemExit('--provenance-json is used with --public-benchmark')
# Refuse target/artifact/metadata errors before allocating any frozen output.
root=fresh(a.output)
for source,name in [(a.input,'input.md'),(a.review,'review.md'),(a.settings_json,'settings.json'),(a.tools_json,'tools.json')]:
 if not source.is_file(): raise SystemExit(f'Missing required artifact: {source}')
 (root/name).write_bytes(source.read_bytes())
record={'kind':'Frozen pre-evaluator review prediction','frozen_utc':utc(),'base':a.base,'head':a.head,'model':a.model,'model_settings':settings,'tools_and_evidence_access':tool_metadata,'fresh_context_per_case':a.fresh_context,'no_hidden_access_before_freeze':a.no_hidden_access,'skill_sha256':tree_hash(a.skill.resolve()),'skill_path':str(a.skill.resolve()),'elapsed_seconds':a.elapsed_seconds,'tokens':a.tokens,'artifacts':{name:sha(root/name) for name in ['input.md','review.md','settings.json','tools.json']},'limits':'Fresh-context attestation and model/tool metadata are caller supplied, not independently authenticated. Frozen copies/hashes detect later edits. Unknown cost must stay null.'}
if a.command_log:
 (root/'commands.log').write_bytes(a.command_log.read_bytes()); record['artifacts']['commands.log']=sha(root/'commands.log')
if a.public_benchmark:
 # Preserve submitted metadata and its source; hashes bind bytes, not authenticity.
 (root/'provenance.json').write_bytes(a.provenance_json.read_bytes())
 (root/'provenance-source.json').write_bytes(provenance_source.read_bytes())
 for name in ['provenance.json','provenance-source.json']: record['artifacts'][name]=sha(root/name)
 record['publication']={'metadata_complete':True,'source_kind':provenance['source']['kind'],'limits':'Caller-supplied envelope and selected host/provider source; tool checks consistency and hashes, not authenticity. Null tokens establish no efficiency claim.'}
save(root/'record.json',record); print(root/'record.json')
