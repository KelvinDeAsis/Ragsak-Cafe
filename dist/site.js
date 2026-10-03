(() => {
  const year = document.querySelector('[data-copyright-year]');
  if (year) year.textContent = new Date().getFullYear();
  const elements = [...document.querySelectorAll('.reveal')];
  const motion = window.matchMedia?.('(prefers-reduced-motion: reduce)');
  let observer;
  const showAll = () => {
    elements.forEach(element => element.classList.remove('reveal-pending'));
    observer?.disconnect();
  };

  // Content stays readable if JavaScript, motion APIs, or observation fail.
  if (!('IntersectionObserver' in window) || !motion || motion.matches) return;
  try {
    observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.remove('reveal-pending');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08 });
    elements.forEach(element => {
      observer.observe(element);
      element.classList.add('reveal-pending');
      element.addEventListener('focusin', () => {
        element.classList.remove('reveal-pending');
        observer.unobserve(element);
      });
    });
    motion.addEventListener?.('change', event => { if (event.matches) showAll(); });
  } catch { showAll(); }
})();
