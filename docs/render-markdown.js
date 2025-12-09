document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('glossary-content');
  if (!container) return;

  const md = window.markdownit({
    html: false,
    linkify: true,
    typographer: true
  });

  fetch('https://raw.githubusercontent.com/Andabeat/tlav-knowledge/refs/heads/main/docs/glossary.md')
    .then((res) => {
      if (!res.ok) throw new Error('Failed to load glossary.md');
      return res.text();
    })
    .then((text) => {
      container.innerHTML = md.render(text);
    })
    .catch((err) => {
      console.error(err);
      container.textContent = 'Error loading glossary.';
    });
});
