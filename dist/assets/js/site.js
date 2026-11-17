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

    /* Two kinds of endpoint, wanting different bodies.
     *
     * A RELATIVE path means Netlify Forms: the submission goes to this site's
     * own origin as url-encoded data and must carry `form-name` so Netlify
     * knows which form it belongs to. Netlify rejects a JSON body outright.
     *
     * An ABSOLUTE URL means a third-party collector — Formspree, Basin, a
     * webhook — and those take JSON.
     *
     * Either way a non-2xx response falls through to the mail client below,
     * so hosting this on something that is not Netlify degrades to the old
     * behaviour instead of losing the enquiry. */
    var ownOrigin = CFG.formEndpoint.charAt(0) === '/';
    var body, headers;

    if (ownOrigin) {
      var params = new URLSearchParams();
      params.append('form-name', form.getAttribute('name') || 'enquiry');
      Object.keys(d).forEach(function (k) {
        /* website is the honeypot; form-name is appended above. */
        if (k !== 'website' && k !== 'form-name') params.append(k, d[k]);
      });
      body = params.toString();
      headers = { 'Content-Type': 'application/x-www-form-urlencoded' };
    } else {
      body = JSON.stringify(d);
      headers = { Accept: 'application/json', 'Content-Type': 'application/json' };
    }

    fetch(CFG.formEndpoint, { method: 'POST', headers: headers, body: body })
      .then(function (r) { if (!r.ok) throw new Error(r.status); form.reset(); say('Thank you — your enquiry has been sent. You will hear back shortly.'); })
      .catch(function () {
        say(CFG.contactEmail ? 'That did not send. Opening your email app instead.' : 'That did not send. Please try again shortly.', 'error');
        if (CFG.contactEmail) window.location.href = mailto(d);
      })
      .finally(function () { submit.disabled = false; });
  });
})();

/* ---------------------------------------------------------------------------
 * Track players — facade embeds.
 *
 * A credit row with data-youtube="VIDEO_ID" gains a play control. Nothing is
 * requested from YouTube until that control is pressed; pressing it IS the
 * consent, which is why no banner is needed for these. The iframe is built
 * once, against youtube-nocookie.com, and reused after that.
 *
 * A row with no data-youtube renders exactly as it did before, so the page is
 * never half-built while IDs are still being gathered.
 * ------------------------------------------------------------------------- */
(function () {
  'use strict';

  // This block is its own IIFE, so it needs its own handle on the config.
  var CFG = window.JB_CONFIG || {};

  /* An ID may come from either place:
   *   - config.js  tracks: { 'JBM—001': 'https://youtu.be/XXXXXXXXXXX' }
   *   - markup     <article class="s-credit" data-youtube="XXXXXXXXXXX">
   * config wins, so a non-technical edit never needs the HTML opened.
   */
  var ID = /^[A-Za-z0-9_-]{11}$/;

  // Accept a bare ID or any ordinary YouTube URL form.
  function idFrom(value) {
    var v = (value || '').trim();
    if (!v) return '';
    if (ID.test(v)) return v;
    // Matches a bare ID, any watch/share/short link, and a whole <iframe>
    // snippet pasted straight from YouTube's Share > Embed panel —
    // including the youtube-nocookie host.
    var m = v.match(/(?:youtube(?:-nocookie)?\.com\/(?:watch\?(?:.*&)?v=|embed\/|shorts\/|live\/)|youtu\.be\/)([A-Za-z0-9_-]{11})/);
    return m ? m[1] : '';
  }

  /* An iframe fires 'load' even when the frame was refused, so the load
   * event cannot tell us whether a video is really playing. Probe instead:
   * ask the browser to fetch a script from youtube.com. If that is refused,
   * this page cannot reach YouTube at all — which is what happens inside a
   * sandboxed preview that blocks third-party frames. Only run it after a
   * click, so nothing contacts YouTube before the visitor asks.
   */
  function probeYouTube(cb) {
    if (window.__jbYT !== undefined) return cb(window.__jbYT);
    var done = function (ok) {
      if (window.__jbYT !== undefined) return;
      window.__jbYT = ok; cb(ok);
    };
    var s = document.createElement('script');
    s.src = 'https://www.youtube.com/iframe_api';
    s.onload = function () { done(true); };
    s.onerror = function () { done(false); };
    document.head.appendChild(s);
    setTimeout(function () { done(false); }, 6000);
  }

  var tracks = CFG.tracks || {};
  var rows = document.querySelectorAll('.s-credit');
  if (!rows.length) return;

  rows.forEach(function (row, i) {
    var cat = (row.querySelector('.s-credit__cat') || {}).textContent || '';
    var id = idFrom(tracks[cat.trim()]) || idFrom(row.getAttribute('data-youtube'));
    if (!id) return;                       // no control, row unchanged

    var title = (row.querySelector('.s-credit__title') || {}).textContent || 'this track';
    var panelId = 'yt-' + i;

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 's-credit__play';
    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('aria-controls', panelId);
    btn.innerHTML = '<span class="tri" aria-hidden="true">&#9654;</span> Watch';
    btn.setAttribute('aria-label', 'Watch ' + title.replace(/[\u201C\u201D]/g, '') + ' on YouTube');

    var panel = document.createElement('div');
    panel.className = 's-credit__player';
    panel.id = panelId;
    panel.hidden = true;
    panel.innerHTML = '<div class="frame"></div>' +
      '<p class="s-credit__note">Plays from YouTube · loaded only when you press play</p>';

    (row.querySelector('.s-credit__roles') || row).insertAdjacentElement('afterend', btn);
    row.appendChild(panel);

    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') === 'true';

      if (open) {
        // Collapse and tear the player down, so nothing keeps playing unseen.
        panel.hidden = true;
        panel.querySelector('.frame').innerHTML = '';
        btn.setAttribute('aria-expanded', 'false');
        btn.innerHTML = '<span class="tri" aria-hidden="true">&#9654;</span> Watch';
        return;
      }

      var frame = panel.querySelector('.frame');
      var note = panel.querySelector('.s-credit__note');
      if (!frame.firstChild) {
        var iframe = document.createElement('iframe');
        // nocookie host, no related-video wall, autoplay because the visitor
        // just asked for it.
        iframe.src = 'https://www.youtube-nocookie.com/embed/' + id + '?rel=0&modestbranding=1&playsinline=1&autoplay=1';
        iframe.title = title + ' — official video on YouTube';
        iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
        iframe.referrerPolicy = 'strict-origin-when-cross-origin';
        iframe.setAttribute('allowfullscreen', '');
        iframe.loading = 'lazy';
        frame.appendChild(iframe);

        note.textContent = 'Loading from YouTube…';
        probeYouTube(function (reachable) {
          note.textContent = reachable
            ? 'Playing here · from YouTube'
            : 'This page cannot reach YouTube, so the video cannot play inline here. '
              + 'That is the preview sandbox, not the site — it plays on the deployed site.';
        });
      }

      // Always offer a way out, whatever the embed does.
      if (!panel.querySelector('.s-credit__out')) {
        var out = document.createElement('p');
        out.className = 's-credit__note s-credit__out';
        out.innerHTML = '<a href="https://www.youtube.com/watch?v=' + id +
          '" target="_blank" rel="noopener">Open on YouTube &#8599;</a>';
        panel.appendChild(out);
      }
      panel.hidden = false;
      btn.setAttribute('aria-expanded', 'true');
      btn.innerHTML = '<span class="tri" aria-hidden="true">&#9632;</span> Close';
      panel.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    });
  });
})();
