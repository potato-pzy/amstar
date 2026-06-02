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

  // ============================================================
  // GOOGLE TRANSLATE INTEGRATION
  // ============================================================

  // 1. Inject Styles dynamically for the Custom Dropdown & Hide Native Google UI
  const styleEl = document.createElement('style');
  styleEl.textContent = `
    /* Hide Google Translate native top banner & tooltips */
    .goog-te-banner-frame,
    .goog-te-banner,
    .skiptranslate:not(.lang-selector-container),
    #goog-gt-tt,
    .goog-te-balloon-frame {
      display: none !important;
    }
    body {
      top: 0px !important;
      position: static !important;
    }
    .goog-text-highlight {
      background-color: transparent !important;
      border: none !important;
      box-shadow: none !important;
    }

    /* Custom Desktop Dropdown styling */
    .lang-selector-container {
      position: relative;
      display: inline-block;
      font-family: 'Alan Sans', sans-serif;
    }
    .lang-selector-btn {
      display: flex;
      align-items: center;
      gap: 8px;
      background: none;
      border: none;
      cursor: pointer;
      padding: 6px 12px;
      border-radius: 20px;
      color: #1a2b4c;
      font-size: 14.5px;
      font-weight: 500;
      transition: all 0.3s ease;
    }
    .lang-selector-btn:hover {
      background-color: rgba(0, 79, 177, 0.08);
      color: #004fb1;
    }
    .lang-selector-btn svg {
      width: 18px;
      height: 18px;
      transition: transform 0.3s ease;
    }
    .lang-selector-btn:hover svg {
      transform: rotate(15deg);
    }
    .lang-dropdown {
      position: absolute;
      top: calc(100% + 8px);
      right: 0;
      background-color: #ffffff;
      border-radius: 8px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
      border: 1px solid rgba(0, 79, 177, 0.08);
      padding: 6px 0;
      min-width: 160px;
      opacity: 0;
      transform: translateY(-10px);
      pointer-events: none;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      z-index: 99999;
    }
    .lang-dropdown.active {
      opacity: 1;
      transform: translateY(0);
      pointer-events: auto;
    }
    .lang-option {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 10px 16px;
      text-decoration: none;
      color: #1a2b4c;
      font-size: 14px;
      font-weight: 400;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .lang-option:hover {
      background-color: rgba(0, 79, 177, 0.05);
      color: #004fb1;
    }
    .lang-option.active {
      color: #004fb1;
      font-weight: 600;
      background-color: rgba(0, 79, 177, 0.03);
    }
    .lang-code {
      font-size: 11px;
      background-color: rgba(0, 79, 177, 0.08);
      color: #004fb1;
      padding: 2px 6px;
      border-radius: 4px;
      text-transform: uppercase;
      font-weight: 600;
    }

    /* Mobile Menu Spacing Adjustment */
    @media (max-width: 991px) {
      #main-nav div[style*="gap: 50px"] {
        gap: 20px !important;
      }
    }
  `;
  document.head.appendChild(styleEl);

  // 2. Cookie Helpers for Google Translate
  function getLanguageFromCookie() {
    const match = document.cookie.match(/googtrans=\/en\/([a-zA-Z\-]+)/);
    return match ? match[1] : null;
  }

  function setLanguage(langCode) {
    const cookieVal = '/en/' + langCode;
    
    // Set cookie for root path and hostname
    document.cookie = "googtrans=" + cookieVal + "; path=/;";
    document.cookie = "googtrans=" + cookieVal + "; path=/; domain=" + window.location.hostname;
    
    // Also try to set for domain variations
    const hostParts = window.location.hostname.split('.');
    if (hostParts.length >= 2) {
      const domain = '.' + hostParts.slice(-2).join('.');
      document.cookie = "googtrans=" + cookieVal + "; path=/; domain=" + domain;
    }
    
    // For English, clean up the cookie
    if (langCode === 'en') {
      document.cookie = "googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
      document.cookie = "googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=" + window.location.hostname;
      if (hostParts.length >= 2) {
        const domain = '.' + hostParts.slice(-2).join('.');
        document.cookie = "googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=" + domain;
      }
    }

    localStorage.setItem('preferred_lang', langCode);
    updateActiveLanguageUI(langCode);

    // Trigger Google Translate native combo change if loaded
    const select = document.querySelector('#google_translate_element select.goog-te-combo');
    if (select) {
      select.value = langCode;
      select.dispatchEvent(new Event('change'));
      // A small timeout to ensure DOM update is forced if translate is already active
      setTimeout(() => {
        if (select.value !== langCode) {
          select.value = langCode;
          select.dispatchEvent(new Event('change'));
        }
      }, 300);
    } else {
      // Fallback reload if Google script isn't initialized yet
      window.location.reload();
    }
  }

  function updateActiveLanguageUI(langCode) {
    // Desktop Button Label Update
    const label = document.querySelector('.active-lang-label');
    if (label) {
      label.textContent = langCode.toUpperCase();
    }
    
    // Desktop Dropdown Options Update
    document.querySelectorAll('.lang-option').forEach(option => {
      if (option.dataset.lang === langCode) {
        option.classList.add('active');
      } else {
        option.classList.remove('active');
      }
    });
    
    // Mobile Overlay Buttons Update
    document.querySelectorAll('.mobile-lang-btn').forEach(btn => {
      if (btn.dataset.lang === langCode) {
        btn.style.backgroundColor = '#004fb1';
        btn.style.color = '#ffffff';
        btn.style.borderColor = '#004fb1';
      } else {
        btn.style.backgroundColor = '#f5f8fc';
        btn.style.color = '#1a2b4c';
        btn.style.borderColor = 'rgba(0, 79, 177, 0.1)';
      }
    });
  }

  // 3. Inject Selectors dynamically into DOM
  function injectLanguageSelectors() {
    // A. Desktop Selector Injection
    const linksGroup = navbar.querySelector('.nav-links')?.parentElement || navbar.querySelector('#mobile-menu-btn')?.parentElement;
    if (linksGroup && !navbar.querySelector('.lang-selector-container')) {
      const container = document.createElement('div');
      container.className = 'lang-selector-container';
      
      const btn = document.createElement('button');
      btn.className = 'lang-selector-btn';
      btn.setAttribute('aria-label', 'Select Language');
      btn.innerHTML = `
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="2" y1="12" x2="22" y2="12"></line>
          <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
        </svg>
        <span class="active-lang-label">EN</span>
      `;
      
      const dropdown = document.createElement('div');
      dropdown.className = 'lang-dropdown';
      
      const languages = [
        { code: 'en', name: 'English', label: 'EN' },
        { code: 'ar', name: 'العربية', label: 'AR' },
        { code: 'es', name: 'Español', label: 'ES' },
        { code: 'fr', name: 'Français', label: 'FR' },
        { code: 'de', name: 'Deutsch', label: 'DE' }
      ];
      
      languages.forEach(lang => {
        const option = document.createElement('a');
        option.className = 'lang-option';
        option.dataset.lang = lang.code;
        option.innerHTML = `
          <span>${lang.name}</span>
          <span class="lang-code">${lang.label}</span>
        `;
        option.addEventListener('click', (e) => {
          e.preventDefault();
          e.stopPropagation();
          setLanguage(lang.code);
          dropdown.classList.remove('active');
        });
        dropdown.appendChild(option);
      });
      
      container.appendChild(btn);
      container.appendChild(dropdown);
      
      // Place right before Contact button (or Hamburger button)
      const contactBtn = linksGroup.querySelector('.nav-cta-btn');
      const mobileBtn = linksGroup.querySelector('#mobile-menu-btn');
      if (contactBtn) {
        linksGroup.insertBefore(container, contactBtn);
      } else if (mobileBtn) {
        linksGroup.insertBefore(container, mobileBtn);
      } else {
        linksGroup.appendChild(container);
      }
      
      // Event listeners for toggle/close
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        dropdown.classList.toggle('active');
      });
      
      document.addEventListener('click', () => {
        dropdown.classList.remove('active');
      });
    }

    // B. Mobile Menu Overlay Injection
    if (mobileMenu && !mobileMenu.querySelector('.mobile-lang-selector')) {
      const mobileLangContainer = document.createElement('div');
      mobileLangContainer.className = 'mobile-lang-selector';
      mobileLangContainer.style.cssText = 'margin-top: 30px; display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; width: 85%;';
      
      const mobileLangs = [
        { code: 'en', name: 'EN' },
        { code: 'ar', name: 'العربية (AR)' },
        { code: 'es', name: 'ES' },
        { code: 'fr', name: 'FR' },
        { code: 'de', name: 'DE' }
      ];
      
      mobileLangs.forEach(lang => {
        const mBtn = document.createElement('button');
        mBtn.dataset.lang = lang.code;
        mBtn.className = 'mobile-lang-btn';
        mBtn.style.cssText = 'background: #f5f8fc; border: 1px solid rgba(0, 79, 177, 0.1); border-radius: 4px; padding: 10px 14px; font-size: 14px; font-weight: 500; color: #1a2b4c; cursor: pointer; transition: all 0.2s;';
        mBtn.textContent = lang.name;
        
        mBtn.addEventListener('click', (e) => {
          e.preventDefault();
          setLanguage(lang.code);
          mobileMenu.classList.remove('active');
        });
        
        mobileLangContainer.appendChild(mBtn);
      });
      
      // Append to the mobile menu
      mobileMenu.appendChild(mobileLangContainer);
    }
  }

  // 4. Initialize Google Translate Client dynamically
  function loadGoogleTranslate() {
    // Check or create container element
    let translateDiv = document.getElementById('google_translate_element');
    if (!translateDiv) {
      translateDiv = document.createElement('div');
      translateDiv.id = 'google_translate_element';
      translateDiv.style.display = 'none';
      document.body.appendChild(translateDiv);
    }
    
    // Register global initialization callback
    window.googleTranslateElementInit = function() {
      new google.translate.TranslateElement({
        pageLanguage: 'en',
        includedLanguages: 'en,ar,es,fr,de',
        layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
        autoDisplay: false
      }, 'google_translate_element');
      
      // Synchronize UI states after initialization
      setTimeout(() => {
        const activeLang = getLanguageFromCookie() || localStorage.getItem('preferred_lang') || 'en';
        updateActiveLanguageUI(activeLang);
        
        // Auto-select native language dropdown to match saved cookie preference
        const select = document.querySelector('#google_translate_element select.goog-te-combo');
        if (select && activeLang !== 'en') {
          select.value = activeLang;
          select.dispatchEvent(new Event('change'));
        }
      }, 800);
    };
    
    // Load external Google script
    const script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = 'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
    document.body.appendChild(script);
  }

  // Trigger setup
  injectLanguageSelectors();
  loadGoogleTranslate();

  // Also hook into initial display synching
  const initialLang = getLanguageFromCookie() || localStorage.getItem('preferred_lang') || 'en';
  updateActiveLanguageUI(initialLang);

})();
