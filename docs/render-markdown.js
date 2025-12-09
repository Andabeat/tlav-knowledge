document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('glossary-content');
  if (!container) return;

  const md = window.markdownit({
    html: false,
    linkify: true,
    typographer: true
  });

  let originalHtml = '';

  fetch('https://raw.githubusercontent.com/Andabeat/tlav-knowledge/refs/heads/main/docs/glossary.md')
    .then((res) => {
      if (!res.ok) throw new Error('Failed to load glossary.md');
      return res.text();
    })
    .then((text) => {
      originalHtml = md.render(text);
      container.innerHTML = originalHtml;

      window.__TLAV_GLOSSARY__ = {
        container,
        getOriginalHtml: () => originalHtml,
        isReady: () => !!originalHtml
      };

      window.dispatchEvent(new Event('tlav_glossary_ready'));
    })
    .catch((err) => {
      console.error(err);
      container.textContent = 'Error loading glossary.';
    });
});
