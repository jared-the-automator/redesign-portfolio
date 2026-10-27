/* =========================================================================
   PETER SCOT DUGOVIC — main.js
   Mobile nav · dropdown · lightbox · comic pager · video · nav state
   ========================================================================= */
(function () {
  'use strict';

  /* ---------------------------------------------------------------
     Mobile navigation
     --------------------------------------------------------------- */
  const toggle = document.querySelector('.nav__toggle');
  const mobile = document.querySelector('.nav__mobile');

  if (toggle && mobile) {
    toggle.addEventListener('click', function () {
      const open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      mobile.classList.toggle('open', !open);
      document.body.style.overflow = open ? '' : 'hidden';
    });

    // Close on link click, deferred to a macrotask. Every menu link is a
    // full-page navigation; hiding the panel synchronously *during* the
    // click's dispatch can make Safari cancel the tap's navigation, so the
    // page the user was on never changes (the menu close "swallows" the tap).
    // Deferring the class toggle out of the dispatch lets the browser commit
    // the navigation first; the fresh page loads with the menu closed.
    mobile.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        setTimeout(function () { toggle.click(); }, 0);
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && mobile.classList.contains('open')) {
        toggle.click();
      }
    });
  }

  /* ---------------------------------------------------------------
     Desktop dropdown (click support for touch)
     --------------------------------------------------------------- */
  function closeAllDropdowns() {
    document.querySelectorAll('.nav__dropdown.open').forEach(function (dropdown) {
      dropdown.classList.remove('open');
    });
  }

  document.querySelectorAll('.nav__dropdown').forEach(function (dd) {
    const trigger = dd.querySelector('.nav__dropdown-trigger');
    if (!trigger) return;
    trigger.addEventListener('click', function (e) {
      e.preventDefault();
      const wasOpen = dd.classList.contains('open');
      closeAllDropdowns();
      if (!wasOpen) dd.classList.add('open');
    });
  });

  // Close dropdowns on outside click
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.nav__dropdown')) {
      closeAllDropdowns();
    }
  });

  /* ---------------------------------------------------------------
     Nav: solid state on scroll + auto-hide
     --------------------------------------------------------------- */
  const SOLID_NAV_SCROLL_OFFSET_PX = 40;
  const HIDE_NAV_SCROLL_OFFSET_PX  = 80;
  const nav = document.querySelector('.nav');
  const hasHero = document.body.classList.contains('has-hero');
  // The comic viewer is an immersive full-viewport section: its nav
  // starts hidden and only reappears when the visitor scrolls up.
  const immersive = !!document.querySelector('.comic');
  let lastScrollY = window.scrollY;

  if (nav) {
    if (immersive) nav.classList.add('nav--hidden');

    const onScroll = function () {
      const y = window.scrollY;

      if (hasHero) {
        nav.classList.toggle('nav--solid', y > SOLID_NAV_SCROLL_OFFSET_PX);
      }

      if (immersive) {
        if (y > lastScrollY && y > HIDE_NAV_SCROLL_OFFSET_PX) {
          nav.classList.add('nav--hidden');
        } else if (y < lastScrollY) {
          nav.classList.remove('nav--hidden');
        }
      } else {
        if (y <= HIDE_NAV_SCROLL_OFFSET_PX) {
          nav.classList.remove('nav--hidden');
        } else if (y > lastScrollY) {
          nav.classList.add('nav--hidden');
        } else {
          nav.classList.remove('nav--hidden');
        }
      }
      lastScrollY = y;
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---------------------------------------------------------------
     Lightbox
     --------------------------------------------------------------- */
  const lightbox = document.querySelector('.lightbox');

  if (lightbox) {
    const imgEl   = lightbox.querySelector('.lightbox__img');
    const capTitle = lightbox.querySelector('.lightbox__caption .title');
    const capMeta  = lightbox.querySelector('.lightbox__caption .meta');
    const counter  = lightbox.querySelector('.lightbox__counter');
    const closeBtn = lightbox.querySelector('.lightbox__close');
    const prevBtn  = lightbox.querySelector('.lightbox__nav--prev');
    const nextBtn  = lightbox.querySelector('.lightbox__nav--next');

    const items = [];
    document.querySelectorAll('[data-lightbox]').forEach(function (el) {
      const i = items.length;
      el.addEventListener('click', function (e) {
        e.preventDefault();
        open(i);
      });
      items.push({
        full:  el.dataset.lightbox,
        title: el.dataset.lbTitle || '',
        meta:  el.dataset.lbMeta  || '',
      });
    });

    let index = 0;

    function render() {
      const it = items[index];
      if (!it) return;
      imgEl.src = it.full;
      capTitle.textContent = it.title;
      capMeta.textContent  = it.meta;
      counter.textContent   = (index + 1) + ' / ' + items.length;
      const navVis = items.length > 1 ? 'visible' : 'hidden';
      prevBtn.style.visibility = navVis;
      nextBtn.style.visibility = navVis;
    }

    function open(i) {
      index = i;
      render();
      lightbox.classList.add('open');
      document.body.style.overflow = 'hidden';
    }

    function close() {
      lightbox.classList.remove('open');
      document.body.style.overflow = '';
    }

    function step(delta) {
      index = (index + delta + items.length) % items.length;
      render();
    }

    closeBtn.addEventListener('click', close);
    prevBtn.addEventListener('click', function () { step(-1); });
    nextBtn.addEventListener('click', function () { step(1); });

    lightbox.addEventListener('click', function (e) {
      if (e.target === lightbox) close();
    });

    document.addEventListener('keydown', function (e) {
      if (!lightbox.classList.contains('open')) return;
      if (e.key === 'Escape')     close();
      if (e.key === 'ArrowLeft')  step(-1);
      if (e.key === 'ArrowRight') step(1);
    });
  }

  /* ---------------------------------------------------------------
     Comic pager
     --------------------------------------------------------------- */
  const comic = document.querySelector('.comic');
  if (comic) {
    const pages = Array.prototype.slice.call(
      comic.querySelectorAll('.comic__page')
    );
    const thumbs = Array.prototype.slice.call(
      comic.querySelectorAll('.comic__thumb')
    );
    const prevBtn  = comic.querySelector('.comic__btn--prev');
    const nextBtn  = comic.querySelector('.comic__btn--next');
    const counter  = comic.querySelector('.comic__counter');
    const progress = comic.querySelector('.comic__progress-bar');

    let current = 0;

    function show(i) {
      if (i < 0 || i >= pages.length) return;

      current = i;

      pages.forEach(function (p, i) {
        p.classList.toggle('is-active', i === current);
        p.classList.toggle('comic__page--prev', i < current);
      });
      thumbs.forEach(function (t, i) {
        t.classList.toggle('is-active', i === current);
      });

      counter.textContent = (current + 1) + ' / ' + pages.length;
      progress.style.width = ((current + 1) / pages.length * 100) + '%';
      prevBtn.disabled = current === 0;
      nextBtn.disabled = current === pages.length - 1;

      const activeThumb = thumbs[current];
      if (activeThumb) activeThumb.scrollIntoView({ inline: 'center', block: 'nearest', behavior: 'smooth' });
    }

    prevBtn.addEventListener('click', function () { show(current - 1); });
    nextBtn.addEventListener('click', function () { show(current + 1); });

    thumbs.forEach(function (t, i) {
      t.addEventListener('click', function () { show(i); });
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft')  show(current - 1);
      if (e.key === 'ArrowRight') show(current + 1);
    });

    // Touch swipe
    const SWIPE_THRESHOLD_PX = 50;
    let startX = null;
    const stage = comic.querySelector('.comic__stage');
    stage.addEventListener('touchstart', function (e) {
      startX = e.touches[0].clientX;
    }, { passive: true });
    stage.addEventListener('touchend', function (e) {
      if (startX === null) return;
      const dx = e.changedTouches[0].clientX - startX;
      if (Math.abs(dx) > SWIPE_THRESHOLD_PX) {
        if (dx < 0) show(current + 1);
        else show(current - 1);
      }
      startX = null;
    }, { passive: true });

    show(0);
  }

  /* ---------------------------------------------------------------
     Card-deck landing (home page)
     --------------------------------------------------------------- */
  const deck = document.querySelector('.deck');
  if (deck) {
    const hero   = deck.querySelector('.deck__card--hero');
    const hint   = deck.querySelector('.deck__hint');
    const slides = Array.prototype.slice.call(deck.querySelectorAll('.deck-slide'));
    const reduceMotion = window.matchMedia
      ? window.matchMedia('(prefers-reduced-motion: reduce)').matches
      : false;

    let dealt = false;

    function showHint(text, visible) {
      if (!hint) return;
      hint.textContent = text;
      hint.classList.toggle('is-on', visible);
    }

    let slideIndex = 0;
    let slideTimer = null;
    function startSlides() {
      if (slides.length < 2 || slideTimer) return;
      slideTimer = setInterval(function () {
        slides[slideIndex].classList.remove('is-active');
        slideIndex = (slideIndex + 1) % slides.length;
        slides[slideIndex].classList.add('is-active');
      }, 4500);
    }

    function deal() {
      if (dealt) return;
      dealt = true;
      deck.classList.remove('is-idle');
      showHint('', false);
      deck.classList.add('is-departed');
      setTimeout(function () {
        deck.classList.add('is-dealt');
        startSlides();
      }, reduceMotion ? 0 : 200);
    }

    if (reduceMotion) {
      deck.classList.add('is-shown', 'is-flipped', 'is-departed', 'is-dealt');
      startSlides();
    } else {
      setTimeout(function () { deck.classList.add('is-shown'); }, 80);
      setTimeout(function () { deck.classList.add('is-flipped'); }, 1400);
      setTimeout(function () {
        deck.classList.add('is-idle');
        showHint('Tap the card', true);
      }, 2200);
      if (hero) {
        hero.addEventListener('click', deal);
      }
    }
  }

  /* ---------------------------------------------------------------
     Video: pause when off-screen (performance)
     --------------------------------------------------------------- */
  function playQuietly(video) {
    const playPromise = video.play();
    if (playPromise && playPromise.catch) {
      playPromise.catch(function (err) {
        // NotAllowedError is expected until the user interacts; let real
        // playback failures propagate instead of hiding them.
        if (err && err.name !== 'NotAllowedError') {
          throw err;
        }
      });
    }
  }

  const videos = document.querySelectorAll('video[data-observe]');
  if ('IntersectionObserver' in window && videos.length) {
    const io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          playQuietly(entry.target);
        } else {
          entry.target.pause();
        }
      });
    }, { threshold: 0.25 });
    videos.forEach(function (v) { io.observe(v); });
  }
})();
