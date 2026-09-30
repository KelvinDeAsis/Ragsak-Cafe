if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
 const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {if(entry.isIntersecting){entry.target.classList.remove('reveal-pending');observer.unobserve(entry.target);}});
 }, {threshold:0.08});
 document.querySelectorAll('.reveal').forEach(element => {element.classList.add('reveal-pending');observer.observe(element);});
}
