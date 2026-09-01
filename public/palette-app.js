/**
 * Palette Theme Selector for study (Astro Starlight)
 * Injects 3 color buttons into the header right-group.
 * Persists choice to localStorage.
 */
(function () {
  const PALETTES = ['amber', 'teal', 'blue'];
  const STORAGE_KEY = 'study:palette';

  function getStored() {
    try { return localStorage.getItem(STORAGE_KEY); } catch { return null; }
  }
  function setStored(p) {
    try { localStorage.setItem(STORAGE_KEY, p); } catch {}
  }

  function applyPalette(palette) {
    document.documentElement.setAttribute('data-palette', palette);
    setStored(palette);
    document.querySelectorAll('.palette-btn').forEach((btn) => {
      btn.classList.toggle('active', btn.dataset.palette === palette);
    });
  }

  function buildUI() {
    const container = document.createElement('div');
    container.className = 'palette-selector';
    container.setAttribute('aria-label', '색상 테마 선택');

    PALETTES.forEach((p) => {
      const btn = document.createElement('button');
      btn.className = 'palette-btn';
      btn.dataset.palette = p;
      btn.setAttribute('aria-label', `${p} 테마`);
      btn.title = { amber: 'Amber', teal: 'Teal', blue: 'Blue' }[p];
      btn.addEventListener('click', () => applyPalette(p));
      container.appendChild(btn);
    });

    return container;
  }

  function mount() {
    const rightGroup = document.querySelector('.header .right-group');
    if (!rightGroup) return;
    if (rightGroup.querySelector('.palette-selector')) return;

    const stored = getStored();
    const initial = PALETTES.includes(stored) ? stored : 'amber';
    applyPalette(initial);

    const ui = buildUI();
    rightGroup.prepend(ui);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount);
  } else {
    mount();
  }
})();
