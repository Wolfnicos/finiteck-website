/* Progressive enhancements. Page content and navigation also work without JavaScript. */
(() => {
  'use strict';

  // Native details menu: close after navigation, outside click, or Escape.
  const menu = document.querySelector('.mobile-nav');
  if (menu) {
    const closeMenu = () => { menu.open = false; };
    menu.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
    document.addEventListener('click', event => {
      if (menu.open && !menu.contains(event.target)) closeMenu();
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && menu.open) {
        closeMenu();
        menu.querySelector('summary').focus();
      }
    });
  }

  const tourImage = document.querySelector('#tour-image');
  const tourLabel = document.querySelector('#tour-label');
  const tourSteps = [...document.querySelectorAll('.tour-step')];
  if (tourImage && tourLabel) {
    let selection = 0;
    tourSteps.forEach(step => step.disabled = false);
    tourSteps.forEach(step => step.addEventListener('click', () => {
      const current = ++selection;
      // Keep the last working image if a new screenshot cannot load.
      const nextImage = new Image();
      nextImage.onload = () => {
        if (current !== selection) return;
        tourImage.src = step.dataset.image;
        tourImage.alt = step.dataset.alt;
        tourLabel.textContent = step.dataset.caption;
        tourSteps.forEach(button => button.setAttribute('aria-pressed', String(button === step)));
      };
      nextImage.src = step.dataset.image;
    }));
  }

  const calculator = document.querySelector('[data-calculator]');
  if (calculator) {
    const spend = calculator.querySelector('#monthly-spend');
    const reduction = calculator.querySelector('#reduction');
    const monthly = calculator.querySelector('#monthly-output');
    const percent = calculator.querySelector('#reduction-output');
    const annual = calculator.querySelector('#yearly-output');
    spend.disabled = false;
    reduction.disabled = false;
    const currency = new Intl.NumberFormat('en-IE', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 });
    let announcement;
    const update = () => {
      const amount = Number(spend.value);
      const rate = Number(reduction.value);
      monthly.textContent = currency.format(amount);
      spend.style.setProperty('--range-fill', `${amount / Number(spend.max) * 100}%`);
      reduction.style.setProperty('--range-fill', `${rate / Number(reduction.max) * 100}%`);
      percent.textContent = `${rate}%`;
      spend.setAttribute('aria-valuetext', `${currency.format(amount)} per month`);
      reduction.setAttribute('aria-valuetext', `${rate} percent`);
      // Debounce the live output so dragging does not queue repeated announcements.
      clearTimeout(announcement);
      announcement = setTimeout(() => {
        annual.replaceChildren(document.createTextNode(`${currency.format(amount * rate / 100 * 12)} `));
        const suffix = document.createElement('small');
        suffix.textContent = '/ year';
        annual.append(suffix);
      }, 100);
    };
    spend.addEventListener('input', update);
    reduction.addEventListener('input', update);
    update();
  }

  const library = document.querySelector('[data-library]');
  if (library) {
    const tools = library.querySelector('[data-library-tools]');
    const search = library.querySelector('#article-search');
    const cards = [...library.querySelectorAll('.article-card')];
    const filters = [...library.querySelectorAll('[data-filter]')];
    const status = library.querySelector('[data-results-status]');
    const empty = library.querySelector('[data-empty-state]');
    const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase('fr').trim();
    const searchable = new Map(cards.map(card => [card, normalize(card.textContent)]));
    let selected = 'all';
    const filter = () => {
      const words = normalize(search.value).split(/\s+/).filter(Boolean);
      let count = 0;
      cards.forEach(card => {
        const matches = (selected === 'all' || card.dataset.category === selected) && words.every(word => searchable.get(card).includes(word));
        card.hidden = !matches;
        if (matches) count++;
      });
      status.textContent = `${count} article${count === 1 ? '' : 's'}${search.value.trim() ? ' pour cette recherche' : ''}`;
      empty.hidden = count !== 0;
      filters.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === selected)));
    };
    tools.hidden = false;
    search.addEventListener('input', filter);
    search.addEventListener('search', filter);
    filters.forEach(button => button.addEventListener('click', () => { selected = button.dataset.filter; filter(); }));
    library.querySelector('[data-reset-search]').addEventListener('click', () => {
      search.value = '';
      selected = 'all';
      filter();
      search.focus();
    });
  }

  const progress = document.querySelector('.reading-progress');
  const article = document.querySelector('[data-reading-article]');
  if (progress && article) {
    let pending = false;
    const updateProgress = () => {
      const bounds = article.getBoundingClientRect();
      const available = Math.max(1, bounds.height - window.innerHeight);
      const fraction = Math.min(1, Math.max(0, -bounds.top / available));
      progress.style.transform = `scaleX(${fraction})`;
      pending = false;
    };
    const schedule = () => {
      if (!pending) {
        pending = true;
        requestAnimationFrame(updateProgress);
      }
    };
    window.addEventListener('scroll', schedule, { passive: true });
    window.addEventListener('resize', schedule, { passive: true });
    updateProgress();
  }
})();
