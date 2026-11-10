/* 홈 화면: 영역별 섹션, 주제 카드, 검색, 영역 칩 */
(function () {
  'use strict';
  var areas = (window.SITE && window.SITE.areas) || [];
  var topics = (window.SITE && window.SITE.topics) || [];
  var wrap = document.getElementById('areas');
  var chips = document.getElementById('chips');
  var input = document.getElementById('homeSearch');
  var empty = document.getElementById('homeEmpty');
  var stat = document.getElementById('homeStat');
  var pick = '전체';

  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }

  function renderChips() {
    var h = '<button type="button" class="chip-btn' + (pick === '전체' ? ' on' : '') + '" data-a="전체">전체 <span>' + topics.length + '</span></button>';
    areas.forEach(function (a) {
      var n = topics.filter(function (t) { return t.area === a.id; }).length;
      h += '<button type="button" class="chip-btn' + (pick === a.id ? ' on' : '') + '" data-a="' + esc(a.id) + '">' + esc(a.name) + ' <span>' + n + '</span></button>';
    });
    chips.innerHTML = h;
  }

  function card(t) {
    return '<a class="card" href="topics/' + esc(t.id) + '/index.html">' +
      '<span class="card-cat">' + esc(t.category || '') + '</span>' +
      '<h3>' + esc(t.title) + '</h3>' +
      '<p>' + esc(t.summary || '') + '</p>' +
      '<span class="card-tags">' + (t.tags || []).slice(0, 5).map(function (x) { return '<i>' + esc(x) + '</i>'; }).join('') + '</span>' +
      '<span class="card-date">' + esc(t.updated || '') + '</span></a>';
  }

  function render() {
    var q = input.value.trim().toLowerCase();
    var html = '', shownTotal = 0;
    areas.forEach(function (a) {
      if (pick !== '전체' && pick !== a.id) return;
      var list = topics.filter(function (t) {
        if (t.area !== a.id) return false;
        if (!q) return true;
        return (t.title + ' ' + (t.summary || '') + ' ' + (t.category || '') + ' ' + (t.tags || []).join(' ')).toLowerCase().indexOf(q) > -1;
      });
      list.sort(function (x, y) { return (y.updated || '').localeCompare(x.updated || ''); });
      var total = topics.filter(function (t) { return t.area === a.id; }).length;
      if (q && !list.length) return;            // 검색 중에는 결과 없는 영역을 숨긴다
      shownTotal += list.length;
      html += '<section class="area-sec" id="area-' + esc(a.id) + '">' +
        '<div class="area-head"><h2>' + esc(a.name) + '</h2><span class="area-count">' + total + '개</span></div>' +
        '<p class="area-desc">' + esc(a.desc || '') + '</p>' +
        (list.length
          ? '<div class="cards">' + list.map(card).join('') + '</div>'
          : '<p class="area-empty">아직 추가된 주제가 없습니다. (준비 중)</p>') +
        '</section>';
    });
    wrap.innerHTML = html;
    empty.hidden = !(q && shownTotal === 0);
    stat.textContent = '영역 ' + areas.length + '개 · 주제 ' + topics.length + '개';
  }

  chips.addEventListener('click', function (e) {
    var b = e.target.closest('.chip-btn'); if (!b) return;
    pick = b.getAttribute('data-a'); renderChips(); render();
  });
  input.addEventListener('input', render);
  renderChips(); render();

  /* 상단 영역 탭(#area-xxx)으로 들어오면 해당 영역으로 스크롤 */
  function goHash() {
    if (location.hash.indexOf('#area-') !== 0) return;
    var id = location.hash.slice(6);
    if (pick !== '전체') { pick = '전체'; renderChips(); render(); }
    var el = document.getElementById('area-' + id);
    if (el) {
      var root = document.documentElement;
      root.style.scrollBehavior = 'auto';      // 영역 이동은 애니메이션 없이 바로
      el.scrollIntoView();
      root.style.scrollBehavior = '';
    }
  }
  window.addEventListener('hashchange', goHash);
  goHash();
})();
