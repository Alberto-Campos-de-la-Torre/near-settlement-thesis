"""Reader decoration is repeatable and preserves executed notebook content."""
import pytest
from near_thesis import notebook,reader


def test_notebook_finalization_is_idempotent_and_preserves_results(tmp_path,monkeypatch):
    (tmp_path/'site').mkdir()
    path=tmp_path/'site/walkthrough.html'
    result='<main><h1>Results</h1><p>Estimate: 1.234</p><pre>preserved output</pre></main>'
    path.write_text('<html lang="en"><head></head><body class="jp-Notebook">'+result+'</body></html>')
    monkeypatch.setattr(notebook,'ROOT',tmp_path)
    notebook.finalize_html();first=path.read_text()
    notebook.finalize_html();second=path.read_text()
    assert first==second
    assert second.count('<nav class="reader-nav"')==1
    assert second.count('<style id="reader-style">')==1
    assert second.count('<script id="reader-theme">')==1
    assert result in second
    assert 'href="index.html"' in second
    assert 'data-reader-theme="dark"' in second


def test_reader_navigation_escapes_label_and_destination():
    markup=reader.navigation('index.html?test="bad"','<unsafe>')
    assert 'aria-label="Back to dashboard"' in markup
    assert '&lt;unsafe&gt;' in markup
    assert '&quot;bad&quot;' in markup
    assert '<unsafe>' not in markup


@pytest.mark.parametrize('existing', ['', ' tabindex="0"'])
def test_existing_notebook_table_becomes_labelled_region(tmp_path,monkeypatch,existing):
    (tmp_path/'site').mkdir()
    path=tmp_path/'site/walkthrough.html'
    path.write_text('<html><head></head><body><main><div class="jp-RenderedHTMLCommon jp-OutputArea-output"'+existing+'><table><tr><td>123</td></tr></table></div><div class="jp-RenderedHTMLCommon jp-OutputArea-output"><table><tr><td>456</td></tr></table></div></main></body></html>')
    monkeypatch.setattr(notebook,'ROOT',tmp_path)
    notebook.finalize_html();notebook.finalize_html()
    result=path.read_text()
    assert result.count('tabindex="0"')==2
    assert result.count('role="region"')==2
    assert result.count('aria-label="Notebook data table 1"')==1
    assert result.count('aria-label="Notebook data table 2"')==1
    assert '<td>123</td>' in result and '<td>456</td>' in result



def test_optional_notebook_scripts_do_not_block_reader_controls(tmp_path,monkeypatch):
    (tmp_path/'site').mkdir()
    path=tmp_path/'site/walkthrough.html'
    path.write_text('<html><head><script src="https://example.invalid/slow.js"></script></head><body><main>Results</main></body></html>')
    monkeypatch.setattr(notebook,'ROOT',tmp_path)
    notebook.finalize_html();first=path.read_text();notebook.finalize_html()
    assert path.read_text()==first
    assert '<script src="https://example.invalid/slow.js" async>' in first
    assert 'Back to dashboard' in first
