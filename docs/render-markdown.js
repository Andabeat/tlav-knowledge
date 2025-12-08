document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('glossary-content');
  const searchInput = document.getElementById('glossary-search');

  if (!container) return;

  const md = window.markdownit({
    html: false,
    linkify: true,
    typographer: true
  });

  let originalHtml = '';
  let plainText = '';

  fetch('./glossary-automation/glossary.md')
    .then((res) => {
      if (!res.ok) throw new Error('Failed to load glossary.md');
      return res.text();
    })
    .then((text) => {
      originalHtml = md.render(text);
      container.innerHTML = originalHtml;

      // For simple search we can also store a plain-text version if needed
      plainText = container.textContent.toLowerCase();
      document.body.classList.remove('is-loading');
    })
    .catch((err) => {
      console.error(err);
      container.textContent = 'Error loading glossary.';
    });

  // Expose a simple API for search.js
  window.__TLAV_GLOSSARY__ = {
    container,
    getOriginalHtml: () => originalHtml,
    isReady: () => !!originalHtml
  };
});
