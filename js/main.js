// Scroll reveal via IntersectionObserver (no scroll listeners)
(function () {
  var els = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window) || !els.length) {
    els.forEach(function (e) { e.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0, rootMargin: '0px 0px -40px 0px' });
    els.forEach(function (e) { io.observe(e); });
    // Safety net: never let content stay hidden (e.g. blocks taller than the viewport)
    window.addEventListener('load', function () {
      setTimeout(function () {
        document.querySelectorAll('.reveal:not(.in)').forEach(function (e) {
          var r = e.getBoundingClientRect();
          if (r.top < window.innerHeight) e.classList.add('in');
        });
      }, 400);
    });
  }

  // Mobile nav toggle
  var toggle = document.querySelector('.nav__toggle');
  var links = document.querySelector('.nav__links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Web3Forms: submit via fetch so the visitor stays on the page
  var form = document.querySelector('form[data-web3form]');
  if (form) {
    var status = form.querySelector('[data-form-status]');
    var btn = form.querySelector('button[type="submit"]');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (status) { status.className = 'form__note'; status.textContent = 'Sending...'; }
      if (btn) { btn.disabled = true; }
      fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { 'Accept': 'application/json' }
      }).then(function (res) {
        return res.json().then(function (data) { return { ok: res.ok, data: data }; });
      }).then(function (r) {
        if (r.ok) {
          form.reset();
          if (status) { status.className = 'form__note is-ok'; status.textContent = 'Thanks. We have your message and will reply within one working day.'; }
        } else {
          if (status) { status.className = 'form__note is-err'; status.textContent = 'Something went wrong. Please email us directly instead.'; }
        }
      }).catch(function () {
        if (status) { status.className = 'form__note is-err'; status.textContent = 'Something went wrong. Please email us directly instead.'; }
      }).finally(function () {
        if (btn) { btn.disabled = false; }
      });
    });
  }
})();
