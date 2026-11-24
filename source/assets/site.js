(function () {
  function ready(fn) { if (document.readyState !== 'loading') fn(); else document.addEventListener('DOMContentLoaded', fn); }
  ready(function () {
    // mobile menu
    var btn = document.querySelector('.menu'), nav = document.getElementById('nav');
    if (btn && nav) btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open'); btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });

    // license search (home + licenses index)
    var q = document.getElementById('lic-search');
    if (q) q.addEventListener('input', function () {
      var v = q.value.trim().toLowerCase();
      document.querySelectorAll('.group').forEach(function (g) {
        var any = false;
        g.querySelectorAll('.lic-list li').forEach(function (li) {
          var hit = !v || li.getAttribute('data-name').indexOf(v) > -1;
          li.classList.toggle('hide', !hit); if (hit) any = true;
        });
        g.classList.toggle('hide', !any);
      });
    });

    // package filter chips
    var chips = document.querySelectorAll('.chip');
    chips.forEach(function (c) {
      c.addEventListener('click', function () {
        chips.forEach(function (x) { x.classList.remove('on'); }); c.classList.add('on');
        var f = c.getAttribute('data-filter');
        document.querySelectorAll('.cards .card').forEach(function (card) {
          card.classList.toggle('hide', f !== 'all' && card.getAttribute('data-type') !== f);
        });
      });
    });

    // contact form (1 Exam Prep form, loaded at runtime so the served HTML has no iframe)
    var fw = document.getElementById('contact-form');
    if (fw) {
      var id = fw.getAttribute('data-form');
      var f = document.createElement('iframe');
      f.src = 'https://app.1examprep.com/widget/form/' + id;
      f.id = 'inline-' + id; f.title = 'Contact form'; f.loading = 'lazy';
      f.setAttribute('data-layout', "{'id':'INLINE'}");
      f.setAttribute('data-form-name', 'Contact ' + fw.getAttribute('data-source'));
      f.setAttribute('data-form-id', id);
      fw.insertBefore(f, fw.firstChild);
      var s = document.createElement('script'); s.src = 'https://app.1examprep.com/js/form_embed.js'; s.async = true;
      document.head.appendChild(s);
    }
  });
})();
