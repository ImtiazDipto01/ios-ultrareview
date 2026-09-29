"""Small dependency-free helpers shared by authored local evaluation fixtures."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess

GIT_ENV = {**os.environ, 'GIT_CONFIG_GLOBAL':os.devnull, 'GIT_CONFIG_NOSYSTEM':'1', 'GIT_AUTHOR_NAME':'Fixture Builder', 'GIT_AUTHOR_EMAIL':'fixture@example.invalid', 'GIT_COMMITTER_NAME':'Fixture Builder', 'GIT_COMMITTER_EMAIL':'fixture@example.invalid'}
def git(repo, *args):
    return subprocess.check_output(['git','-c','core.hooksPath=/dev/null','-c','commit.gpgsign=false','-C',str(repo),*args], env=GIT_ENV, text=True).strip()
def write(repo, files):
    for name, content in files.items():
        path=Path(repo)/name; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(content)
def init(repo, files):
    Path(repo).mkdir(parents=True)
    git(repo,'init','--quiet','--template=','-b','base')
    write(repo,files)
    return commit(repo,'Establish component and existing consumers')
def commit(repo, message):
    git(repo,'add','.'); git(repo,'commit','--quiet','-m',message)
    return git(repo,'rev-parse','HEAD')
def fresh(path):
    path=Path(path).resolve()
    if path.exists() and any(path.iterdir()): raise SystemExit(f'Refusing non-empty output: {path}')
    path.mkdir(parents=True,exist_ok=True); return path
def save(path, data):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    Path(path).write_text(json.dumps(data,indent=2)+'\n')
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def tree_hash(root):
    items=[(str(p.relative_to(root)),sha(p)) for p in sorted(Path(root).rglob('*')) if p.is_file() and not any(x in p.parts for x in ('.git','.build','__pycache__')) and p.name!='.DS_Store']
    return hashlib.sha256(json.dumps(items,separators=(',',':')).encode()).hexdigest()
def utc(): return datetime.now(timezone.utc).isoformat()
def execute(command,cwd,log,env=None):
    started=utc()
    result=subprocess.run(command,cwd=cwd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    Path(log).parent.mkdir(parents=True,exist_ok=True); Path(log).write_text(result.stdout)
    return {'command':command,'working_directory':str(cwd),'started_utc':started,'completed_utc':utc(),'exit_code':result.returncode,'log':str(log),'log_sha256':sha(log)}
def prompt(repo,base,head,extra=''):
    return f'''Review this complete local snapshot with the assigned iOS UltraReview skill. Produce a draft; do not post externally.

Repository: `{repo}`
Base: `{base}`
Head: `{head}`
Stated intent and documented checks: `PRODUCT.md` and `README.md` at this target.

Acquire the entire diff and affected consumers. Preserve the ordinary checkout. Inspect dependencies, executable infrastructure, attributes and Git trust settings before materialization/execution. Locally authored dependency-free checks may run when their inspected contents are suitable. Do not claim simulator, device or CI results that were not executed or supplied.

Only this input, this repository, the assigned skill, and explicitly supplied evidence are review input. Do not inspect sibling repositories, generator source, suite manifests, evaluator files, hidden tests or prior evaluation conclusions. Review artifacts must be frozen before evaluator access. The full component impact radius is present; do not invent omitted production systems.
{extra}
'''

def execute_json(command,cwd,log):
    """Keep structured stdout separate from diagnostic stderr, with both retained."""
    started=utc()
    result=subprocess.run(command,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    Path(log).parent.mkdir(parents=True,exist_ok=True); Path(log).write_text(result.stdout)
    stderr=Path(str(log)+'.stderr.log'); stderr.write_text(result.stderr)
    return {'command':command,'working_directory':str(cwd),'started_utc':started,'completed_utc':utc(),'exit_code':result.returncode,'log':str(log),'log_sha256':sha(log),'stderr_log':str(stderr),'stderr_sha256':sha(stderr)}
