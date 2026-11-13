"""Stage an explicit allowlist of rebuilt public pages for GitHub Pages."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]

def package(destination=None):
    destination = Path(destination) if destination else ROOT/'.pages'
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    pages = [Path('index.html'), Path('walkthrough.html'), Path('THESIS.html'), Path('README.html')]
    pages += [p.relative_to(ROOT).with_suffix('.html') for p in (ROOT/'docs').glob('*.md')]
    pages += [p.relative_to(ROOT).with_suffix('.html') for p in (ROOT/'data/bigquery').glob('**/README.md')]
    pages += [p.relative_to(ROOT) for p in (ROOT/'docs/assets').glob('*.png')]
    for relative in pages:
        source = ROOT/'site'/relative
        target = destination/relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    (destination/'.nojekyll').write_text('')
    print(f'Public Pages bundle: {len(pages)} files; no raw workspace/cache/media files.')
    return destination

if __name__ == '__main__':
    package()
