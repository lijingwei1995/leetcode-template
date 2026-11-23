
(function () {
  'use strict';

  // 复制代码
  document.querySelectorAll('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var card = btn.closest('.code-card');
      if (!card) return;
      var body = card.querySelector('.code-body');
      var text = Array.prototype.map.call(body.querySelectorAll('.lt'), function (el) {
        return el.textContent.replace(/\u00a0/g, '');
      }).join('\n');
      var done = function () {
        var old = btn.textContent;
        btn.textContent = '已复制';
        setTimeout(function () { btn.textContent = old; }, 1500);
      };
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(done, function () { fallback(text, done); });
      } else {
        fallback(text, done);
      }
    });
  });

  function fallback(text, done) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); done(); } catch (e) {}
    document.body.removeChild(ta);
  }

  // 导航页筛选
  var search = document.getElementById('search');
  if (search) {
    var rows = Array.prototype.slice.call(document.querySelectorAll('.problem-row'));
    var sections = Array.prototype.slice.call(document.querySelectorAll('.category'));
    var chips = Array.prototype.slice.call(document.querySelectorAll('[data-diff-filter]'));
    var tplFilter = document.getElementById('tplFilter');
    var countEl = document.getElementById('resultCount');
    var emptyEl = document.getElementById('emptyState');
    var state = { diff: 'all', tpl: 'all', q: '' };

    function apply() {
      var visible = 0;
      rows.forEach(function (row) {
        var okDiff = state.diff === 'all' || row.dataset.diff === state.diff;
        var okTpl = state.tpl === 'all' || row.dataset.tpl.split(' ').indexOf(state.tpl) !== -1;
        var okQ = !state.q || row.dataset.search.toLowerCase().indexOf(state.q) !== -1;
        var ok = okDiff && okTpl && okQ;
        row.hidden = !ok;
        if (ok) visible++;
      });
      sections.forEach(function (sec) {
        var any = Array.prototype.some.call(sec.querySelectorAll('.problem-row'), function (r) { return !r.hidden; });
        sec.hidden = !any;
      });
      if (countEl) countEl.textContent = visible + ' / ' + rows.length + ' 题';
      if (emptyEl) emptyEl.hidden = visible !== 0;
    }

    search.addEventListener('input', function () {
      state.q = search.value.trim().toLowerCase();
      apply();
    });
    chips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        state.diff = chip.dataset.diffFilter;
        chips.forEach(function (c) { c.classList.toggle('active', c === chip); });
        apply();
      });
    });
    if (tplFilter) {
      tplFilter.addEventListener('change', function () {
        state.tpl = tplFilter.value;
        apply();
      });
    }
    document.addEventListener('keydown', function (e) {
      if (e.key === '/' && document.activeElement !== search) {
        e.preventDefault();
        search.focus();
      }
    });
    apply();
  }

  // 目录高亮
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll('.toc a'));
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var map = {};
    tocLinks.forEach(function (a) {
      var id = a.getAttribute('href').slice(1);
      var sec = document.getElementById(id);
      if (sec) map[id] = a;
    });
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          tocLinks.forEach(function (a) { a.classList.remove('active'); });
          var a = map[entry.target.id];
          if (a) a.classList.add('active');
        }
      });
    }, { rootMargin: '-15% 0px -70% 0px', threshold: 0 });
    Object.keys(map).forEach(function (id) { obs.observe(document.getElementById(id)); });
  }
})();
