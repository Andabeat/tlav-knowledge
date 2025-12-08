document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('glossary-search');

  if (!searchInput || !window.__TLAV_GLOSSARY__) return;

  const { container } = window.__TLAV_GLOSSARY__;

  function applyFilter(query) {
    const q = query.trim().toLowerCase();
    const sections = [];

    // Build sections: each h2 plus its following siblings until next h1/h2
    const nodes = Array.from(container.children);
    let current = null;

    nodes.forEach((node) => {
      if (node.tagName === 'H2') {
        current = { heading: node, nodes: [node] };
        sections.push(current);
      } else if (current) {
        current.nodes.push(node);
      }
    });

    if (!q) {
      // Show everything
      sections.forEach((section) => {
        section.nodes.forEach((n) => {
          n.style.display = '';
        });
      });
      document.body.classList.remove('is-filtering');
      return;
    }

    document.body.classList.add('is-filtering');

    sections.forEach((section) => {
      const text = section.nodes
        .map((n) => n.textContent.toLowerCase())
        .join(' ');

      const match = text.includes(q);

      section.nodes.forEach((n) => {
        n.style.display = match ? '' : 'none';
      });
    });
  }

  searchInput.addEventListener('input', (e) => {
    if (!window.__TLAV_GLOSSARY__.isReady()) return;
    applyFilter(e.target.value);
  });
});
