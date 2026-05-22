(() => {
  const navbar = document.getElementById('main-nav');
  if (!navbar) return;

  const menuBtn = document.getElementById('mobile-menu-btn');
  const closeBtn = document.querySelector('#mobile-menu .close-btn');
  const mobileMenu = document.getElementById('mobile-menu');

  if (menuBtn && mobileMenu) {
    menuBtn.addEventListener('click', () => {
      mobileMenu.classList.add('active');
    });
  }

  if (closeBtn && mobileMenu) {
    closeBtn.addEventListener('click', () => {
      mobileMenu.classList.remove('active');
    });
  }

  let lastScrollY = 0;
  let ticking = false;

  function setNavbarStyle(scrollY, direction) {
    if (scrollY < 5) {
      navbar.style.top = '40px';
      navbar.style.left = '50%';
      navbar.style.transform = 'translateX(-50%)';
      navbar.style.width = '90%';
      navbar.style.maxWidth = '1300px';
      navbar.style.borderRadius = '4px';
      navbar.style.padding = '15px 40px';
      navbar.style.boxShadow = '0 10px 30px rgba(0,0,0,0.08)';
      navbar.style.opacity = '1';
      navbar.style.pointerEvents = '';
    } else {
      if (navbar.style.left !== '0px' && navbar.style.left !== '0') {
        navbar.style.left = '0';
        navbar.style.transform = 'none';
        navbar.style.width = '100%';
        navbar.style.maxWidth = '100%';
        navbar.style.borderRadius = '0';
        navbar.style.padding = '12px 5%';
        navbar.style.boxShadow = '0 4px 15px rgba(0,0,0,0.1)';
      }
      if (direction === 'down') {
        navbar.style.top = '-90px';
        navbar.style.opacity = '0';
        navbar.style.pointerEvents = 'none';
      } else {
        navbar.style.top = '0';
        navbar.style.opacity = '1';
        navbar.style.pointerEvents = '';
      }
    }
  }

  window.addEventListener('scroll', () => {
    const currentScrollY = window.scrollY || window.pageYOffset;
    const direction = currentScrollY > lastScrollY ? 'down' : 'up';
    if (!ticking) {
      window.requestAnimationFrame(() => {
        setNavbarStyle(currentScrollY, direction);
        lastScrollY = currentScrollY;
        ticking = false;
      });
      ticking = true;
    }
  }, { passive: true });

  setNavbarStyle(window.scrollY || 0, 'up');
})();
