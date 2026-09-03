/**
 * Palette Theme Selector for study (Astro Starlight)
 * Injects a modern <select> dropdown into the header right-group.
 * Persists choice to localStorage.
 */
(function () {
  const PALETTES = [
    { id: 'indigo', label: 'Slate Indigo' },
    { id: 'cyan', label: 'Nordic Cyan' },
    { id: 'blue', label: 'Zinc Blue' },
    { id: 'sand', label: 'Warm Sand' },
  ];
  const STORAGE_KEY = 'study:palette';

  function getStored() {
    try {
      return localStorage.getItem(STORAGE_KEY);
    } catch {
      return null;
    }
  }
  function setStored(p) {
    try {
      localStorage.setItem(STORAGE_KEY, p);
    } catch {}
  }

  function applyPalette(palette) {
    document.documentElement.setAttribute('data-palette', palette);
    setStored(palette);
    const select = document.querySelector('.palette-select');
    if (select && select.value !== palette) {
      select.value = palette;
    }
  }

  function buildUI() {
    const container = document.createElement('div');
    container.className = 'palette-select-container';

    const select = document.createElement('select');
    select.className = 'palette-select';
    select.setAttribute('aria-label', '색상 테마 선택');
    select.title = '색상 테마 선택';

    PALETTES.forEach(({ id, label }) => {
      const option = document.createElement('option');
      option.value = id;
      option.textContent = label;
      select.appendChild(option);
    });

    select.addEventListener('change', (e) => {
      applyPalette(e.target.value);
    });

    container.appendChild(select);
    return container;
  }

  function mount() {
    const rightGroup = document.querySelector('.header .right-group');
    if (!rightGroup) return;
    if (rightGroup.querySelector('.palette-select-container')) return;

    const stored = getStored();
    const initial = PALETTES.some((p) => p.id === stored) ? stored : 'indigo';
    applyPalette(initial);

    const ui = buildUI();
    const select = ui.querySelector('.palette-select');
    if (select) select.value = initial;

    rightGroup.prepend(ui);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount);
  } else {
    mount();
  }
})();
