/* 모든 페이지 공통: 테마, 영역 탭(상단), 하위 탭(같은 영역의 주제들), 노션 링크 */
(function () {
  'use strict';
  var root = document.documentElement;
  var ROOT = document.body.getAttribute('data-root') || './';
  var CURRENT = document.body.getAttribute('data-topic') || '';
  var SITE = window.SITE || { name: '나의 공부 공간', areas: [], topics: [] };
  var areas = SITE.areas || [];
  var topics = SITE.topics || [];

  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
  function find(arr, id) { return arr.filter(function (x) { return x.id === id; })[0]; }

  var curTopic = CURRENT ? find(topics, CURRENT) : null;
  var curAreaId = curTopic ? curTopic.area : '';

  /* ---------- Theme ---------- */
  function applyTheme(t) { if (t) root.setAttribute('data-theme', t); else root.removeAttribute('data-theme'); }
  function currentTheme() {
    var t = root.getAttribute('data-theme');
    if (t) return t;
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  try { var saved = localStorage.getItem('study-theme'); if (saved) applyTheme(saved); } catch (e) {}
  var themeBtn = document.getElementById('themeBtn');
  if (themeBtn) themeBtn.addEventListener('click', function () {
    var next = currentTheme() === 'dark' ? 'light' : 'dark';
    applyTheme(next);
    try { localStorage.setItem('study-theme', next); } catch (e) {}
  });

  /* ---------- 글자 크기 (모든 페이지에 같은 값 적용, 선택값 저장) ---------- */
  var SIZES = [80, 90, 100, 110, 120, 135, 150];
  var sizePct = 100;
  try { var sv = parseInt(localStorage.getItem('study-fontscale'), 10); if (SIZES.indexOf(sv) >= 0) sizePct = sv; } catch (e) {}
  function applySize() { root.style.fontSize = sizePct === 100 ? '' : sizePct + '%'; }
  applySize();
  if (themeBtn && themeBtn.parentNode) {
    var wrap = document.createElement('span');
    wrap.className = 'size-btns';
    wrap.innerHTML = '<button type="button" class="icon-btn" id="sizeDown" aria-label="글자 작게" title="글자 작게">A−</button>' +
                     '<button type="button" class="icon-btn size-val" id="sizeVal" aria-label="글자 크기 100%로" title="클릭하면 100%로"></button>' +
                     '<button type="button" class="icon-btn" id="sizeUp" aria-label="글자 크게" title="글자 크게">A+</button>';
    themeBtn.parentNode.insertBefore(wrap, themeBtn);
    var sizeVal = wrap.querySelector('#sizeVal');
    var showSize = function () { sizeVal.textContent = sizePct + '%'; };
    var setSize = function (p) {
      sizePct = p; applySize(); showSize();
      try { localStorage.setItem('study-fontscale', String(p)); } catch (e) {}
      setHeaderH();
    };
    showSize();
    wrap.querySelector('#sizeDown').addEventListener('click', function () { var i = SIZES.indexOf(sizePct); if (i > 0) setSize(SIZES[i - 1]); });
    wrap.querySelector('#sizeUp').addEventListener('click', function () { var i = SIZES.indexOf(sizePct); if (i < SIZES.length - 1) setSize(SIZES[i + 1]); });
    sizeVal.addEventListener('click', function () { setSize(100); });
  }

  /* ---------- Brand + 영역 탭 ---------- */
  var brand = document.getElementById('brand');
  if (brand) { brand.href = ROOT + 'index.html'; brand.textContent = SITE.name; }

  var tabs = document.getElementById('tabs');
  function renderTabs() {
    if (!tabs) return;
    var hashArea = (location.hash.indexOf('#area-') === 0) ? location.hash.slice(6) : '';
    var onHome = !CURRENT;
    var activeArea = curAreaId || (onHome ? hashArea : '');
    var h = '<a class="tab' + (onHome && !hashArea ? ' active' : '') + '" href="' + ROOT + 'index.html">홈</a>';
    areas.forEach(function (a) {
      var n = topics.filter(function (t) { return t.area === a.id; }).length;
      h += '<a class="tab' + (a.id === activeArea ? ' active' : '') + (n ? '' : ' empty') + '" href="' + ROOT + 'index.html#area-' + esc(a.id) + '"' +
           (a.id === curAreaId ? ' aria-current="true"' : '') + '>' + esc(a.name) + '</a>';
    });
    tabs.innerHTML = h;
    var active = tabs.querySelector('.tab.active');
    if (active) {
      var ar = active.getBoundingClientRect(), tr = tabs.getBoundingClientRect();
      if (ar.left < tr.left || ar.right > tr.right) tabs.scrollLeft += ar.left - tr.left - 16;
    }
  }
  renderTabs();
  window.addEventListener('hashchange', renderTabs);

  /* ---------- 하위 탭: 현재 영역의 주제들 (주제 페이지에서만) ---------- */
  var header = document.querySelector('.site-header');
  if (header && curTopic) {
    var area = find(areas, curAreaId);
    var sib = topics.filter(function (t) { return t.area === curAreaId; });
    var sub = document.createElement('nav');
    sub.id = 'subtabs'; sub.className = 'subrow'; sub.setAttribute('aria-label', '같은 영역의 주제');
    var sh = '<span class="sub-label">' + esc(area ? area.name : '') + '</span>';
    sib.forEach(function (t) {
      var on = t.id === CURRENT;
      sh += '<a class="subtab' + (on ? ' active' : '') + '" href="' + ROOT + 'topics/' + esc(t.id) + '/index.html"' +
            (on ? ' aria-current="page"' : '') + ' title="' + esc(t.title) + '">' + esc(t.short || t.title) + '</a>';
    });
    sub.innerHTML = sh;
    header.appendChild(sub);
    var act = sub.querySelector('.subtab.active');
    if (act) {
      var r1 = act.getBoundingClientRect(), r2 = sub.getBoundingClientRect();
      if (r1.left < r2.left || r1.right > r2.right) sub.scrollLeft += r1.left - r2.left - 16;
    }
  }

  /* ---------- 헤더 높이를 CSS 변수로 (사이드바·앵커 위치 계산용) ---------- */
  function setHeaderH() {
    if (header) root.style.setProperty('--header-h', header.offsetHeight + 'px');
  }
  setHeaderH();
  window.addEventListener('resize', setHeaderH);
  window.addEventListener('load', setHeaderH);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(setHeaderH);

  /* ---------- Notion link / 수정일 (주제 페이지 하단) ---------- */
  var nl = document.getElementById('notionLink');
  if (nl && curTopic && curTopic.notion) { nl.href = curTopic.notion; nl.hidden = false; }
  var upd = document.getElementById('updatedAt');
  if (upd && curTopic && curTopic.updated) upd.textContent = '마지막 수정 ' + curTopic.updated;
})();
