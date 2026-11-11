/* Theme travels with local links even when browser storage is unavailable. */
(() => {
  const valid = value => ['light', 'dark', 'auto'].includes(value);
  const fromQuery = new URLSearchParams(location.search).get('theme');
  let saved = '';
  if (valid(fromQuery)) saved = fromQuery === 'auto' ? '' : fromQuery;
  else { try { saved = localStorage.getItem('theme') || ''; } catch (_) {} }
  if (!['', 'light', 'dark'].includes(saved)) saved = '';
  if (saved) document.documentElement.dataset.theme = saved;
  const decorateLink = anchor => {
    const url = new URL(anchor.href, location.href);
    if (url.protocol !== location.protocol || url.host !== location.host || !url.pathname.endsWith('.html')) return;
    url.searchParams.set('theme', document.documentElement.dataset.theme || 'auto');
    const version = document.querySelector('meta[name="reader-version"]')?.content;
    if (version) url.searchParams.set('v', version);
    anchor.href = url.href;
  };
  const apply = theme => {
    if (!['', 'light', 'dark'].includes(theme)) theme = '';
    if (theme) document.documentElement.dataset.theme = theme;
    else document.documentElement.removeAttribute('data-theme');
    document.querySelectorAll('[data-reader-theme]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.readerTheme === theme)));
    try { localStorage.setItem('theme', theme); } catch (_) {}
    try { const url = new URL(location.href); url.searchParams.set('theme', theme || 'auto'); history.replaceState(null, '', url); } catch (_) {}
    document.querySelectorAll('a.reader-back').forEach(decorateLink);
  };
  document.addEventListener('click', event => {
    const anchor = event.target.closest('a[href]');
    if (anchor) decorateLink(anchor);
  });
  const initialize = () => {
    apply(saved);
    document.querySelectorAll('[data-reader-theme]').forEach(button => button.addEventListener('click', () => apply(button.dataset.readerTheme)));
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialize, { once: true });
  else initialize();
})();
