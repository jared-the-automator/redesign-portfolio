// The Wooden Bird: carousels, gallery filter, lightbox, nav. No dependencies.
(() => {
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Mobile nav
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const open = nav.dataset.open === "true";
      nav.dataset.open = String(!open);
      toggle.setAttribute("aria-expanded", String(!open));
    });
  }

  // Generic crossfade carousel. Markup: [data-carousel] with [data-slide] children,
  // optional [data-sync] groups that follow the same index, and prev/next/pause buttons.
  document.querySelectorAll("[data-carousel]").forEach((root) => {
    const slides = [...root.querySelectorAll("[data-slide]")];
    const synced = [...root.querySelectorAll("[data-sync]")];
    const count = root.querySelector("[data-count]");
    const caption = root.querySelector("[data-caption]");
    const pauseBtn = root.querySelector("[data-pause]");
    const interval = Number(root.dataset.interval || 6500);
    if (slides.length < 2) return;
    let i = 0, timer = null, paused = reduced;

    const show = (n) => {
      i = (n + slides.length) % slides.length;
      slides.forEach((s, k) => {
        s.classList.toggle("is-active", k === i);
        s.setAttribute("aria-hidden", String(k !== i));
      });
      synced.forEach((s) => {
        const kids = [...s.children];
        kids.forEach((c, k) => c.classList.toggle("is-active", k === i % kids.length));
      });
      if (count) count.textContent = `${i + 1} / ${slides.length}`;
      if (caption) caption.textContent = slides[i].dataset.label || "";
    };
    const start = () => { stop(); if (!paused) timer = setInterval(() => show(i + 1), interval); };
    const stop = () => { if (timer) clearInterval(timer); timer = null; };

    root.querySelector("[data-prev]")?.addEventListener("click", () => { show(i - 1); start(); });
    root.querySelector("[data-next]")?.addEventListener("click", () => { show(i + 1); start(); });
    pauseBtn?.addEventListener("click", () => {
      paused = !paused;
      pauseBtn.setAttribute("aria-pressed", String(paused));
      pauseBtn.setAttribute("aria-label", paused ? "Play slideshow" : "Pause slideshow");
      pauseBtn.textContent = paused ? "▶" : "❚❚";
      paused ? stop() : start();
    });
    if (pauseBtn && reduced) {
      pauseBtn.setAttribute("aria-pressed", "true");
      pauseBtn.setAttribute("aria-label", "Play slideshow");
      pauseBtn.textContent = "▶";
    }
    root.addEventListener("focusin", stop);
    root.addEventListener("focusout", start);
    show(0);
    start();
  });

  // Process steps drive the photo stack
  document.querySelectorAll("[data-process]").forEach((root) => {
    const steps = [...root.querySelectorAll(".steps li")];
    const figs = [...root.querySelectorAll(".process-stack figure")];
    const activate = (k) => {
      steps.forEach((s, n) => s.classList.toggle("is-active", n === k));
      figs.forEach((f, n) => f.classList.toggle("is-active", n === k));
    };
    steps.forEach((s, k) => {
      s.querySelector("button")?.addEventListener("click", () => activate(k));
    });
    if ("IntersectionObserver" in window) {
      const io = new IntersectionObserver((entries) => {
        entries.forEach((e) => { if (e.isIntersecting) activate(steps.indexOf(e.target)); });
      }, { rootMargin: "-45% 0px -45% 0px" });
      steps.forEach((s) => io.observe(s));
    }
    activate(0);
  });

  // Gallery filter + species note
  const gallery = document.querySelector("[data-gallery]");
  if (gallery) {
    const chips = [...document.querySelectorAll("[data-filter]")];
    const figs = [...gallery.querySelectorAll("figure[data-species]")];
    const notes = [...document.querySelectorAll("[data-note]")];
    const apply = (slug, push) => {
      chips.forEach((c) => c.setAttribute("aria-pressed", String(c.dataset.filter === slug)));
      figs.forEach((f) => { f.hidden = slug !== "all" && !f.dataset.species.split(" ").includes(slug); });
      notes.forEach((n) => { n.hidden = n.dataset.note !== slug; });
      if (push) history.replaceState(null, "", slug === "all" ? location.pathname : `?species=${slug}`);
      const live = document.getElementById("gallery-status");
      if (live) live.textContent = `${figs.filter((f) => !f.hidden).length} pieces shown`;
    };
    chips.forEach((c) => c.addEventListener("click", () => apply(c.dataset.filter, true)));
    const initial = new URLSearchParams(location.search).get("species");
    apply(chips.some((c) => c.dataset.filter === initial) ? initial : "all", false);

    // Lightbox
    const dlg = document.querySelector("dialog.lightbox");
    if (dlg) {
      const img = dlg.querySelector("img");
      const cap = dlg.querySelector("[data-lb-caption]");
      gallery.querySelectorAll("button[data-full]").forEach((b) => {
        b.addEventListener("click", () => {
          img.src = b.dataset.full;
          img.alt = b.querySelector("img").alt;
          cap.textContent = b.closest("figure").querySelector("figcaption")?.textContent || "";
          dlg.showModal();
        });
      });
      dlg.querySelector("[data-close]").addEventListener("click", () => dlg.close());
      dlg.addEventListener("click", (e) => { if (e.target === dlg) dlg.close(); });
    }
  }

  // Reveal on scroll
  if (!reduced && "IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    document.querySelectorAll(".reveal").forEach((el) => io.observe(el));
  } else {
    document.querySelectorAll(".reveal").forEach((el) => el.classList.add("is-in"));
  }
})();
