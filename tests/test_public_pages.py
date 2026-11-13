"""The deployment artifact must not inherit arbitrary files from the build folder."""
from pathlib import Path
import importlib.util


def test_pages_allowlist_excludes_stale_pages_credentials_and_video(tmp_path, monkeypatch):
    script = Path(__file__).resolve().parents[1]/'tools/package_site.py'
    spec = importlib.util.spec_from_file_location('public_pages', script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, 'ROOT', tmp_path)
    (tmp_path/'docs/assets').mkdir(parents=True)
    (tmp_path/'docs/METHOD.md').write_text('# Method')
    (tmp_path/'docs/assets/dashboard.png').write_bytes(b'public image')
    for name in ['index.html','walkthrough.html','THESIS.html','README.html','docs/METHOD.html','docs/assets/dashboard.png', '.env', 'demo.mp4','docs/FINAL_REVIEW_CHECKLIST.html']:
        target = tmp_path/'site'/name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b'public page' if name.endswith('.html') else b'fixture')
    bundle = module.package()
    files = {p.relative_to(bundle).as_posix() for p in bundle.rglob('*') if p.is_file()}
    assert files == {'.nojekyll','index.html','walkthrough.html','THESIS.html','README.html','docs/METHOD.html','docs/assets/dashboard.png'}
