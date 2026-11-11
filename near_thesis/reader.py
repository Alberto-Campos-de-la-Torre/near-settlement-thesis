"""Shared reader navigation and theme assets for local research pages."""
import hashlib
from html import escape
from pathlib import Path

WEB = Path(__file__).parent / 'web'


def version() -> str:
    paths = [Path(__file__), WEB/'reader.js', WEB/'review-docs.css', WEB.parent/'notebook.py', WEB.parent/'documentation.py']
    return hashlib.sha256(b''.join(path.read_bytes() for path in paths)).hexdigest()[:12]


def head() -> str:
    return (f'<meta id="reader-version" name="reader-version" content="{version()}">'
            '<style id="reader-style">' + (WEB/'review-docs.css').read_text() + '</style>'
            '<script id="reader-theme">' + (WEB/'reader.js').read_text() + '</script>')


def navigation(back: str, label: str) -> str:
    return (f'<nav class="reader-nav" aria-label="Documentation">'
            f'<a class="reader-back" aria-label="Back to dashboard" href="{escape(back, quote=True)}">'
            '<span class="reader-arrow" aria-hidden="true">↖</span>'
            '<span><small>FROM CLICKS TO SETTLEMENT</small><strong>Back to dashboard</strong></span></a>'
            f'<div class="reader-tools"><span class="reader-label">{escape(label)}</span>'
            '<div class="reader-theme" role="group" aria-label="Reading theme">'
            '<button data-reader-theme="" aria-pressed="true">Auto</button>'
            '<button data-reader-theme="light" aria-pressed="false">Light</button>'
            '<button data-reader-theme="dark" aria-pressed="false">Dark</button>'
            '</div></div></nav>')
