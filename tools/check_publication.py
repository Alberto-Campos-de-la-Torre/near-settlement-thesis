"""Reject private credentials and production media from the public Git tree.

Before initial Git setup, inspect the curated working tree. After setup, inspect
all tracked files, including ignored files if they were accidentally force-added.
Never print a matched credential value.
"""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MEDIA = {'.mp4', '.webm', '.mov', '.mkv', '.avi', '.mp3', '.wav', '.flac', '.m4a', '.srt', '.vtt', '.ass', '.pem', '.key', '.p12', '.pfx', '.jks'}
RULES = {
    'private key': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'GitHub token': re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b'),
    'personal email': re.compile(r'\b[A-Za-z0-9._%+-]+@(?!(?:users\.noreply\.github\.com|example\.(?:com|org|net))\b)[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'),
    'signing credential': re.compile(r'ed25519:[1-9A-HJ-NP-Za-km-z]{80,}'),
    'AWS access identifier': re.compile(r'\bAKIA[A-Z0-9]{16}\b'),
    'Google API key': re.compile(r'\bAIza[A-Za-z0-9_-]{30,}\b'),
    'private cloud project': re.compile(r'near-thesis-\d{5,}'),
    'private query job': re.compile(r'\bbqjob_[A-Za-z0-9_]{12,}'),
    'private local path': re.compile(r'/home/(?!runner/)[A-Za-z0-9_-]+/'),
}

def main():
    result = subprocess.run(['git', 'ls-files', '-z'], cwd=ROOT, capture_output=True)
    paths = [ROOT / p for p in result.stdout.decode().split('\0') if p] if result.returncode == 0 else [p for p in ROOT.rglob('*') if p.is_file() and not any(x in p.parts for x in ('.git', '.venv', '__pycache__', '.pytest_cache'))]
    failures = []
    for path in paths:
        rel = path.relative_to(ROOT)
        name = path.name.lower()
        if path.suffix.lower() in MEDIA or name.startswith('.env') or name.startswith('demo_') or name in {'record_demo.py', 'finish_export.py'} or 'credentials' in name or 'service-account' in name or any(p.startswith('demo-video') for p in rel.parts):
            failures.append((str(rel), 'excluded private/production file'))
        if not path.exists():
            failures.append((str(rel), 'missing tracked file'))
            continue
        content = path.read_bytes()
        if b'\0' in content:
            continue
        content = content.decode('utf-8', errors='replace')
        for rule, pattern in RULES.items():
            if pattern.search(content):
                failures.append((str(rel), rule))
    for path, rule in failures:
        print(f'FAIL {path}: {rule}')
    print(f'Publication guard: {len(paths)} files checked; {len(failures)} violations.')
    return bool(failures)

if __name__ == '__main__':
    raise SystemExit(main())
