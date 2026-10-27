(() => {
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
