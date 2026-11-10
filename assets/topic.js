(function () {
  'use strict';

  var root = document.documentElement;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* 주제 페이지 공통 동작: 사이드바 목차, 스크롤 추적, 이미지 확대, (있으면) 용어 검색
     테마와 상단 탭은 common.js 가 처리합니다. */

  /* ---------- Build TOC ---------- */
  var toc = document.getElementById('toc');
  var heads = $$('.part-banner, h2, h3', $('.content'));
  var html = '<ul>';
  var openH3 = false;
  heads.forEach(function (h) {
    var id = h.id; if (!id) return;
    var label = h.textContent.trim();
    if (h.classList.contains('part-banner')) {
      if (openH3) { html += '</ul></li>'; openH3 = false; }
      html += '<li class="toc-part-wrap"><div class="toc-part">' + label.replace(/ — .*/, '') + '</div></li>';
    } else if (h.tagName === 'H2') {
      if (openH3) { html += '</ul></li>'; openH3 = false; }
      html += '<li data-h2="' + id + '"><a href="#' + id + '" data-id="' + id + '">' + label + '</a>';
      var hasKids = false, n = h.closest('section');
      if (n && n.querySelector('h3')) hasKids = true;
      if (hasKids) { html += '<ul class="toc-h3" data-parent="' + id + '">'; openH3 = true; }
      else html += '</li>';
    } else if (h.tagName === 'H3') {
      html += '<li><a href="#' + id + '" data-id="' + id + '">' + label + '</a></li>';
    }
  });
  if (openH3) html += '</ul></li>';
  html += '</ul>';
  toc.innerHTML = html;

  var links = {};
  $$('a[data-id]', toc).forEach(function (a) { links[a.dataset.id] = a; });

  /* ---------- Scroll spy ---------- */
  var tracked = heads.filter(function (h) { return h.id && links[h.id]; });
  var currentId = null;
  function setActive(id) {
    if (id === currentId) return;
    currentId = id;
    $$('a.active', toc).forEach(function (a) { a.classList.remove('active'); });
    $$('.toc-h3.open', toc).forEach(function (u) { u.classList.remove('open'); });
    var a = links[id]; if (!a) return;
    a.classList.add('active');
    var parentId = id.indexOf('-') > -1 ? 's' + id.slice(1).split('-')[0] : id;
    var kids = $('.toc-h3[data-parent="' + parentId + '"]', toc);
    if (kids) kids.classList.add('open');
    if (links[parentId] && parentId !== id) links[parentId].classList.add('active');
    // keep active item visible in the sidebar
    var sb = document.getElementById('sidebar');
    var r = a.getBoundingClientRect(), sr = sb.getBoundingClientRect();
    if (r.top < sr.top + 60 || r.bottom > sr.bottom - 40) {
      sb.scrollTop += r.top - sr.top - sr.height / 3;
    }
  }
  function onScroll() {
    var hdr = document.querySelector('.site-header');
    var y = window.scrollY + (hdr ? hdr.offsetHeight : 56) + 24, found = null;
    for (var i = 0; i < tracked.length; i++) {
      if (tracked[i].getBoundingClientRect().top + window.scrollY <= y) found = tracked[i].id; else break;
    }
    if (found) setActive(found);
    var max = document.documentElement.scrollHeight - window.innerHeight;
    var bar = document.getElementById('progress');
    if (bar) bar.style.width = (max > 0 ? Math.min(100, window.scrollY / max * 100) : 0) + '%';
    var tt = document.getElementById('toTop');
    if (tt) tt.hidden = window.scrollY < 600;
  }
  var ticking = false;
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; requestAnimationFrame(function () { onScroll(); ticking = false; }); }
  }, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();

  /* ---------- Re-align hash target after web fonts reflow the page ---------- */
  function realign() {
    if (!location.hash) return;
    var t = null;
    try { t = document.getElementById(decodeURIComponent(location.hash.slice(1))); } catch (e) {}
    if (!t) return;
    root.style.scrollBehavior = 'auto';
    t.scrollIntoView();
    root.style.scrollBehavior = '';
    onScroll();
  }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(realign);
  window.addEventListener('load', realign);

  /* ---------- Mobile menu ---------- */
  var menuBtn = document.getElementById('menuBtn');
  function setMenu(open) {
    document.body.classList.toggle('menu-open', open);
    if (menuBtn) { menuBtn.setAttribute('aria-expanded', String(open)); menuBtn.textContent = open ? '✕' : '☰'; }
  }
  if (menuBtn) menuBtn.addEventListener('click', function () { setMenu(!document.body.classList.contains('menu-open')); });
  document.getElementById('scrim').addEventListener('click', function () { setMenu(false); });
  toc.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });

  /* ---------- To top ---------- */
  var tt = document.getElementById('toTop');
  if (tt) tt.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });

  /* ---------- Lightbox ---------- */
  var lb = document.getElementById('lightbox');
  var lbImg = $('img', lb), lbCap = $('.lb-cap', lb);
  function openLb(img) {
    lbImg.src = img.currentSrc || img.src;
    lbImg.alt = img.alt;
    var cap = img.closest('figure').querySelector('figcaption');
    lbCap.textContent = cap ? cap.textContent : '';
    lb.hidden = false;
    document.body.style.overflow = 'hidden';
  }
  function closeLb() { lb.hidden = true; lbImg.removeAttribute('src'); document.body.style.overflow = ''; }
  $$('figure img').forEach(function (img) { img.addEventListener('click', function () { openLb(img); }); });
  lb.addEventListener('click', function (e) { if (e.target !== lbImg) closeLb(); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { if (!lb.hidden) closeLb(); else setMenu(false); }
  });

  /* ---------- Glossary search ---------- */
  var input = document.getElementById('glossSearch');
  if (!input) return;
  var rows = $$('#glossary tbody tr');
  var count = document.getElementById('glossCount');
  var empty = document.getElementById('glossEmpty');
  var original = rows.map(function (tr) { return Array.prototype.map.call(tr.cells, function (c) { return c.textContent; }); });
  function esc(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function filter() {
    var q = input.value.trim().toLowerCase(), shown = 0;
    rows.forEach(function (tr, i) {
      var cells = original[i];
      var hit = !q || cells.join(' ').toLowerCase().indexOf(q) > -1;
      tr.hidden = !hit;
      if (hit) shown++;
      Array.prototype.forEach.call(tr.cells, function (td, j) {
        var t = cells[j];
        if (!q) { td.textContent = t; return; }
        var idx = t.toLowerCase().indexOf(q);
        if (idx < 0) { td.textContent = t; return; }
        td.innerHTML = esc(t.slice(0, idx)) + '<mark>' + esc(t.slice(idx, idx + q.length)) + '</mark>' + esc(t.slice(idx + q.length));
      });
    });
    count.textContent = q ? shown + ' / ' + rows.length + '개' : rows.length + '개 용어';
    empty.hidden = shown !== 0;
  }
  input.addEventListener('input', filter);
  filter();
})();
