(() => {
  const year = document.querySelector('[data-copyright-year]');
  if (year) year.textContent = new Date().getFullYear();
  // Responsive link behavior is independent of animation preferences.
  // Coarse touch input also covers phones held in landscape orientation.
  const mobile = window.matchMedia?.('(max-width: 767px), (hover: none) and (pointer: coarse)');
  const externalLinks = [...document.querySelectorAll('a[href^="https://"]')]
    .filter(link => new URL(link.href).origin !== window.location.origin);
  const setLinkTargets = () => externalLinks.forEach(link => {
    const newTab = mobile && !mobile.matches;
    link.setAttribute('target', newTab ? '_blank' : '_self');
    link.setAttribute('rel', 'noopener noreferrer');
    if (newTab) link.setAttribute('title', 'Opens in a new tab');
    else link.removeAttribute('title');
  });
  setLinkTargets();
  mobile?.addEventListener?.('change', setLinkTargets);
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
