/* J BOWMAN — shared behaviour for the guidelines and the site.
 * Every behaviour here is an enhancement; both render fully without it.
 * The one exception is form submission, which degrades to a plain instruction.
 */
(function () {
  'use strict';

  var CFG = window.JB_CONFIG || {};

  /* --- Navigation ------------------------------------------------------- */

  var toggle = document.querySelector('.nav__toggle');
  var links = document.getElementById('nav-links');

  if (toggle && links) {
    var wide = function () { return window.matchMedia('(min-width: 60.01rem)').matches; };
    var label = toggle.textContent.trim() || 'Menu';

    var setOpen = function (open) {
      toggle.setAttribute('aria-expanded', String(open));
      toggle.textContent = open ? 'Close' : label;
      links.hidden = wide() ? false : !open;
    };

    setOpen(false);
    toggle.addEventListener('click', function () {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });
    links.addEventListener('click', function (e) {
      if (e.target.closest('a') && !wide()) setOpen(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') { setOpen(false); toggle.focus(); }
    });
    window.addEventListener('resize', function () {
      if (wide()) { links.hidden = false; toggle.setAttribute('aria-expanded', 'false'); }
      else if (toggle.getAttribute('aria-expanded') !== 'true') { links.hidden = true; }
    });
  }

  /* --- Reveal ----------------------------------------------------------- */

  if (document.documentElement.classList.contains('js')) {
    var targets = document.querySelectorAll('.reveal');
    if (targets.length && 'IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          en.target.classList.add('is-in');
          io.unobserve(en.target);
        });
      }, { rootMargin: '0px 0px -10% 0px', threshold: 0.05 });
      targets.forEach(function (el) { io.observe(el); });

      // Safety net — content must never be left invisible by a missed callback.
      var sweep = function () {
        targets.forEach(function (el) {
          if (el.getBoundingClientRect().top < window.innerHeight * 1.1) el.classList.add('is-in');
        });
      };
      requestAnimationFrame(sweep);
      window.addEventListener('load', sweep);
    }
  }

  /* --- Section tracking in the nav -------------------------------------- */

  var anchors = Array.prototype.slice.call(document.querySelectorAll('.nav__links a[href^="#"]'));
  if (anchors.length && 'IntersectionObserver' in window) {
    var sections = anchors.map(function (a) { return document.querySelector(a.getAttribute('href')); }).filter(Boolean);
    var seen = new Set();
    var mark = function () {
      var cur = sections.find(function (s) { return seen.has(s.id); });
      anchors.forEach(function (a) {
        if (cur && a.getAttribute('href') === '#' + cur.id) a.setAttribute('aria-current', 'true');
        else if (a.getAttribute('aria-current') === 'true') a.removeAttribute('aria-current');
      });
    };
    var nav = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { en.isIntersecting ? seen.add(en.target.id) : seen.delete(en.target.id); });
      mark();
    }, { rootMargin: '-20% 0px -60% 0px' });
    sections.forEach(function (s) { nav.observe(s); });
  }

  /* --- Configured links -------------------------------------------------- */

  var social = CFG.social || {};
  document.querySelectorAll('[data-social]').forEach(function (node) {
    var url = social[node.getAttribute('data-social')];
    if (!url) return;                                     // stays plain text
    var a = document.createElement('a');
    a.href = url; a.textContent = node.textContent; a.rel = 'me noopener'; a.target = '_blank';
    node.replaceWith(a);
  });

  document.querySelectorAll('[data-contact-email]').forEach(function (node) {
    if (!CFG.contactEmail) return;                        // keeps the placeholder visible
    var a = document.createElement('a');
    a.href = 'mailto:' + CFG.contactEmail;
    a.textContent = CFG.contactEmail;
    a.className = node.className;
    node.replaceWith(a);
  });

  /* --- Enquiry form ------------------------------------------------------ */

  var form = document.getElementById('enquiry');
  if (!form) return;

  var status = form.querySelector('.form__status');
  var submit = form.querySelector('button[type="submit"]');
  var say = function (msg, tone) { status.textContent = msg; status.setAttribute('data-tone', tone || 'info'); };

  var slotFor = function (field) { return form.querySelector('#' + field.id + '-error'); };
  var setError = function (field, msg) { field.setAttribute('aria-invalid', 'true'); var s = slotFor(field); if (s) s.textContent = msg; };
  var clearError = function (field) { field.removeAttribute('aria-invalid'); var s = slotFor(field); if (s) s.textContent = ''; };

  form.querySelectorAll('input, select, textarea').forEach(function (f) {
    f.addEventListener('input', function () { clearError(f); });
  });

  var validate = function () {
    var first = null;
    form.querySelectorAll('[required]').forEach(function (f) {
      clearError(f);
      var v = f.value.trim();
      var bad = !v || (f.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v));
      if (bad) {
        setError(f, f.type === 'email' && v ? 'Enter a valid email address.' : 'This field is required.');
        if (!first) first = f;
      }
    });
    if (first) first.focus();
    return !first;
  };

  var fields = function () { var d = {}; new FormData(form).forEach(function (v, k) { d[k] = v; }); return d; };

  var mailto = function (d) {
    var body = ['Name: ' + d.name, 'Email: ' + d.email, 'Company: ' + (d.company || '—'),
                'Type of enquiry: ' + (d.enquiryType || '—'), '', d.project || ''].join('\n');
    return 'mailto:' + CFG.contactEmail +
      '?subject=' + encodeURIComponent('Enquiry — ' + (d.enquiryType || 'General') + ' — ' + d.name) +
      '&body=' + encodeURIComponent(body);
  };

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!validate()) { say('Check the highlighted fields.', 'error'); return; }

    var d = fields();
    if (d.website) return;                                // honeypot

    if (!CFG.formEndpoint && !CFG.contactEmail) {
      say('This form is not connected yet. Set contactEmail in assets/js/config.js, or reach J Bowman through the profiles below.', 'error');
      return;
    }
    if (!CFG.formEndpoint) {
      window.location.href = mailto(d);
      say('Opening your email app with the enquiry ready to send.');
      return;
    }

    submit.disabled = true;
    say('Sending…');
    fetch(CFG.formEndpoint, {
      method: 'POST',
      headers: { Accept: 'application/json', 'Content-Type': 'application/json' },
      body: JSON.stringify(d)
    })
      .then(function (r) { if (!r.ok) throw new Error(r.status); form.reset(); say('Thank you — your enquiry has been sent. You will hear back shortly.'); })
      .catch(function () {
        say(CFG.contactEmail ? 'That did not send. Opening your email app instead.' : 'That did not send. Please try again shortly.', 'error');
        if (CFG.contactEmail) window.location.href = mailto(d);
      })
      .finally(function () { submit.disabled = false; });
  });
})();
