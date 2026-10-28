(() => {
  // A direct link to the implementation section should reveal its contents.
  const revealHashTarget = () => {
    if (!location.hash) return;
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    if (!target) return;
    const disclosure = target.matches('details') ? target : target.closest('details');
    if (disclosure) disclosure.open = true;
  };
  revealHashTarget();
  window.addEventListener('hashchange', revealHashTarget);
  document.querySelectorAll('a[href="#implementation"]').forEach((link) => {
    link.addEventListener('click', () => {
      const section = document.getElementById('implementation');
      if (section) section.open = true;
    });
  });
  document.querySelectorAll('img[data-fallback]').forEach((img) => {
    const fallback = () => {
      if (!img.dataset.fallback) return;
      img.src = img.dataset.fallback;
      if (img.dataset.fallbackAlt) img.alt = img.dataset.fallbackAlt;
      delete img.dataset.fallback;
      delete img.dataset.fallbackAlt;
    };
    img.addEventListener('error', fallback, { once: true });
    if (img.complete && !img.naturalWidth) fallback();
  });
  const filters = document.querySelector('.filters');
  if (!filters) return;
  const rows = [...document.querySelectorAll('[data-category]')];
  filters.hidden = false;
  filters.addEventListener('click', (event) => {
    const button = event.target.closest('button[data-filter]');
    if (!button) return;
    const category = button.dataset.filter;
    filters.querySelectorAll('button').forEach((b) => {
      const active = b === button;
      b.classList.toggle('active', active);
      b.setAttribute('aria-pressed', String(active));
    });
    rows.forEach((row) => { row.hidden = category !== 'All' && row.dataset.category !== category; });
    document.getElementById('filter-result').textContent = `${rows.filter((r) => !r.hidden).length} projects shown.`;
  });
})();
