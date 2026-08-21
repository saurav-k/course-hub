/* ============================================================================
   outline.js - the route runtime for this course.

   Every other course in the hub ships a static `window.COURSE_OUTLINE` that the
   shared rail in assets/hub.js renders. This course has four outlines over one
   pool of pages, so it ships the pool and the four routes as data in routes.js
   and derives the outline here, at load time, from whichever route is active.
   Nothing in hub.js needed changing: it still finds one COURSE_OUTLINE and one
   script whose src ends in outline.js.

   Three rules this file implements, in order of importance.

   1. A lesson has exactly one URL. The route is a query parameter on that URL,
      never part of the path. lessons/0024-x.html is the same page in all four
      routes.
   2. A shared link preserves the route. The URL carries ?route= whenever the
      active route is not the default one, so copying the address bar always
      shares the lens you are reading in. The default route needs no parameter,
      which keeps the canonical URL clean.
   3. Without JavaScript the page is still complete. The route switcher is four
      real links, the pager and breadcrumb are rendered statically for the route
      that owns the page, and the course map shows all four routes stacked. This
      file only marks the active route, re-points navigation at it, and carries
      the parameter across links.
   ========================================================================= */
(function () {
  'use strict';

  var MANIFEST = window.COURSE_ROUTES;
  if (!MANIFEST) return;

  var PARAM = 'route';
  var STORE_KEY = 'coursehub.route.' + MANIFEST.key;

  /* Storage can throw on file:// and with site data blocked, so it is optional
     everywhere. A reader without it gets a working page that forgets the lens. */
  function get(key) { try { return window.localStorage.getItem(key); } catch (e) { return null; } }
  function set(key, value) { try { window.localStorage.setItem(key, value); } catch (e) { /* ignore */ } }

  function routeById(id) {
    for (var i = 0; i < MANIFEST.routes.length; i++) {
      if (MANIFEST.routes[i].id === id) return MANIFEST.routes[i];
    }
    return null;
  }

  function fileOf(path) { return path.split('#')[0].split('?')[0].split('/').pop(); }

  function filesOf(route) {
    var files = [];
    route.sections.forEach(function (section) {
      section.lessons.forEach(function (file) { files.push(file); });
    });
    return files;
  }

  function routeHas(route, file) { return filesOf(route).indexOf(file) !== -1; }

  /* The route whose order this page's static navigation already follows: the
     first route in the manifest that contains it. validate_site.py enforces
     that the committed pager and breadcrumb agree with this same rule. */
  function homeRoute(file) {
    for (var i = 0; i < MANIFEST.routes.length; i++) {
      if (routeHas(MANIFEST.routes[i], file)) return MANIFEST.routes[i];
    }
    return routeById(MANIFEST['default']);
  }

  function paramRoute() {
    var query = window.location.search;
    if (!query) return null;
    var pairs = query.replace(/^\?/, '').split('&');
    for (var i = 0; i < pairs.length; i++) {
      var pair = pairs[i].split('=');
      if (decodeURIComponent(pair[0]) === PARAM) return decodeURIComponent(pair[1] || '');
    }
    return null;
  }

  /* ---- resolve the active route ------------------------------------------
     The URL wins over the stored preference, which wins over the default. A
     route named in the URL is also remembered, so following a shared link
     switches the lens rather than fighting it. */
  var fromUrl = paramRoute();
  var active = routeById(fromUrl) ? fromUrl : null;
  if (active) {
    set(STORE_KEY, active);
  } else {
    var stored = get(STORE_KEY);
    active = routeById(stored) ? stored : MANIFEST['default'];
  }
  var activeRoute = routeById(active);

  /* Set before the body is parsed, so the course map never flashes all four
     route outlines before settling on one. */
  document.documentElement.setAttribute('data-route', active);

  function decorate(href) {
    return active === MANIFEST['default'] ? href : href + '?' + PARAM + '=' + active;
  }

  /* ---- the outline the shared rail renders ------------------------------- */
  window.COURSE_OUTLINE = {
    key: MANIFEST.key,
    title: MANIFEST.title,
    sections: activeRoute.sections.map(function (section) {
      return {
        n: section.n,
        title: section.title,
        lessons: section.lessons.map(function (file) {
          return { title: MANIFEST.pages[file].title, href: decorate('lessons/' + file) };
        })
      };
    }),
    extras: MANIFEST.extras
  };

  /* ---- everything below needs the document -------------------------------- */
  function courseBase() {
    var tag = document.querySelector('script[src$="outline.js"]');
    return tag ? new URL('.', tag.src).href : new URL('.', window.location.href).href;
  }

  function ready(fn) {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
    else fn();
  }

  ready(function () {
    var base = courseBase();
    var lessonBase = new URL('lessons/', base).href;
    var here = fileOf(window.location.pathname);
    var onLesson = Object.prototype.hasOwnProperty.call(MANIFEST.pages, here);
    var pageRoute = onLesson && !routeHas(activeRoute, here) ? homeRoute(here) : activeRoute;

    /* 1. Canonical URL. Stamp the parameter when the lens is not the default,
       strip it when it is, so the address bar is always shareable and always
       minimal. replaceState can be refused on some file:// origins; a failure
       costs the stamp and nothing else. */
    try {
      var url = new URL(window.location.href);
      var wanted = active === MANIFEST['default'] ? null : active;
      var current = url.searchParams.get(PARAM);
      if (wanted !== current) {
        if (wanted) url.searchParams.set(PARAM, wanted); else url.searchParams.delete(PARAM);
        window.history.replaceState(null, '', url.pathname + url.search + url.hash);
      }
    } catch (e) { /* the page works without a tidy address bar */ }

    /* 2. Carry the lens across every link that stays inside this course's pool,
       and leave cross-course and external links alone. */
    if (active !== MANIFEST['default']) {
      var links = document.querySelectorAll('a[href]');
      for (var i = 0; i < links.length; i++) {
        var link = links[i];
        var raw = link.getAttribute('href');
        if (!raw || raw.charAt(0) === '#' || raw.indexOf('?') !== -1) continue;
        var resolved;
        try { resolved = new URL(raw, window.location.href); } catch (e) { continue; }
        if (resolved.href.indexOf(lessonBase) !== 0) continue;
        if (!Object.prototype.hasOwnProperty.call(MANIFEST.pages, fileOf(resolved.pathname))) continue;
        link.setAttribute('href', raw + '?' + PARAM + '=' + active);
      }
    }

    /* 3. The route switcher: mark the active lens for assistive technology.
       Which one looks active is CSS, driven by the attribute set in the head. */
    var bar = document.querySelector('.routebar');
    if (bar) {
      var tabs = bar.querySelectorAll('a[data-route]');
      for (var t = 0; t < tabs.length; t++) {
        if (tabs[t].getAttribute('data-route') === active) tabs[t].setAttribute('aria-current', 'true');
        else tabs[t].removeAttribute('aria-current');
      }
    }

    /* 4. Re-point the pager at the active route. The committed markup already
       holds the route that owns this page, so this is a no-op when they agree. */
    var pager = document.querySelector('.pager[data-pager-route]');
    if (pager && onLesson && pager.getAttribute('data-pager-route') !== pageRoute.id) {
      var order = filesOf(pageRoute);
      var at = order.indexOf(here);
      var ends = pager.querySelectorAll('a');
      if (ends.length === 2 && at !== -1) {
        writeEnd(ends[0], at > 0 ? order[at - 1] : null, '← Previous');
        writeEnd(ends[1], at < order.length - 1 ? order[at + 1] : null, 'Next →');
        pager.setAttribute('data-pager-route', pageRoute.id);
      }
    }

    function writeEnd(anchor, file, direction) {
      var dir = anchor.querySelector('.dir');
      var ttl = anchor.querySelector('.ttl');
      if (dir) dir.textContent = direction;
      if (file) {
        anchor.setAttribute('href', decorate(file));
        if (ttl) ttl.textContent = MANIFEST.pages[file].title;
      } else {
        anchor.setAttribute('href', '../index.html');
        if (ttl) ttl.textContent = 'Course map';
      }
    }

    /* 5. The breadcrumb names the section of the route being read, which is the
       part of a lesson's identity that genuinely changes with the lens. */
    var crumb = document.querySelector('[data-crumb-section]');
    if (crumb && onLesson) {
      for (var s = 0; s < pageRoute.sections.length; s++) {
        if (pageRoute.sections[s].lessons.indexOf(here) !== -1) {
          crumb.textContent = pageRoute.sections[s].title;
          break;
        }
      }
    }
  });
}());
