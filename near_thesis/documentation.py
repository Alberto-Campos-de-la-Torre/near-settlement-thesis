"""Package English reviewer documentation alongside the offline dashboard."""
from __future__ import annotations

import html
import os
from pathlib import Path
import re
import shutil
from urllib.parse import unquote, urlsplit

from .config import ROOT, SITE, REPO_URL
from . import reader


def run(destination: Path = SITE) -> None:
    # Already locked through notebook export and declared directly for this
    # renderer. No remote service, new package version or HTTP request is used.
    import mistune

    sources = [ROOT/'README.md', ROOT/'THESIS.md', *sorted((ROOT/'docs').glob('*.md')),
               *sorted((ROOT/'audit').glob('**/README.md')), *sorted((ROOT/'data/bigquery').glob('**/README.md'))]
    outputs = {source.resolve(): destination/source.relative_to(ROOT).with_suffix('.html') for source in sources}
    # Bundle the public dashboard capture for offline README rendering.
    for asset in (ROOT/'docs'/'assets').glob('*.png'):
        target = destination/'docs'/'assets'/asset.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(asset, target)
    reader_head = reader.head()

    for source, output in outputs.items():
        class Renderer(mistune.HTMLRenderer):
            def __init__(self):
                super().__init__(escape=True)
                self.ids = {}

            def heading(self, text, level, **attrs):
                plain = html.unescape(re.sub(r'<[^>]+>', '', text))
                slug = re.sub(r'[^\w\- ]', '', plain.lower()).replace(' ', '-')
                count = self.ids.get(slug, 0)
                self.ids[slug] = count + 1
                anchor = slug + (f'-{count}' if count else '')
                return f'<h{level} id="{html.escape(anchor, quote=True)}">{text}</h{level}>\n'

            def link(self, text, url, title=None):
                parsed = urlsplit(url)
                target = None
                if not parsed.scheme and parsed.path:
                    target = (source.parent/unquote(parsed.path)).resolve()
                elif url.startswith('https://github.com/NGZeggers/near-value-shift/blob/main/'):
                    target = (ROOT/unquote(parsed.path.split('/blob/main/', 1)[1])).resolve()
                if target in outputs:
                    url = Path(os.path.relpath(outputs[target], output.parent)).as_posix()
                    if parsed.fragment:
                        url += '#' + parsed.fragment
                elif target and target.is_relative_to(ROOT) and target.exists():
                    # Machine evidence remains the original repository resource;
                    # no credentials, caches or unrelated local files are copied.
                    url = REPO_URL + '/blob/main/' + target.relative_to(ROOT).as_posix()
                    if parsed.fragment:
                        url += '#' + parsed.fragment
                return super().link(text, url, title)

        markdown = mistune.create_markdown(renderer=Renderer(), plugins=['table', 'strikethrough'])
        text = source.read_text()
        first = next((line.lstrip('# ').strip() for line in text.splitlines() if line.startswith('# ')), source.stem)
        back = Path(os.path.relpath(destination/'index.html', output.parent)).as_posix()
        page = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width, initial-scale=1">'
                f'<title>{html.escape(first)}</title>{reader_head}</head><body>'
                + reader.navigation(back, 'Research notes') +
                f'<main>{markdown(text)}</main></body></html>\n')
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(page)
    print(f'English review documents: {len(outputs)} local HTML pages')
