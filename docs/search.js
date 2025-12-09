document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('glossary-search');
  if (!searchInput) return;

  function attachSearch(glossary) {
    const { container } = glossary;

    function applyFilter(query) {
      const q = query.trim().toLowerCase();
      const items = Array.from(container.querySelectorAll('p'));

      if (!q) {
        items.forEach((p) => {
          p.style.display = '';
        });
        document.body.classList.remove('is-filtering');
        return;
      }

      document.body.classList.add('is-filtering');

      items.forEach((p) => {
        const text = p.textContent.toLowerCase();
        const match = text.includes(q);
        p.style.display = match ? '' : 'none';
      });
    }

    searchInput.addEventListener('input', (e) => {
      if (!glossary.isReady()) return;
      applyFilter(e.target.value);
    });
  }

  if (window.__TLAV_GLOSSARY__) {
    attachSearch(window.__TLAV_GLOSSARY__);
  } else {
    window.addEventListener('tlav_glossary_ready', () => {
      attachSearch(window.__TLAV_GLOSSARY__);
    });
  }
});
