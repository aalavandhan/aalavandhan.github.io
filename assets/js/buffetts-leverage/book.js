// "Letter book" modals: excerpts from Berkshire's shareholder letters, typewritten across the two
// open, unruled, age-yellowed pages of an old brown-covered book. Any dialog with class "blv-book" gets the look. Markup:
//
//   Buffett has said so in his [annual letters](#modal-letters-assets).
//
//   <dialog id="modal-letters-assets" class="modal blv-book">
//   <div class="spread">
//   <div class="page left">
//     <p class="head">In their own words</p>
//     <blockquote><p>A passage from a letter.</p><cite>Warren Buffett, 1989</cite></blockquote>
//   </div>
//   <div class="page right">
//     <blockquote><p>Something said outright.</p><cite>Charlie Munger, 2019</cite></blockquote>
//   </div>
//   </div>
//   </dialog>
//
// Sign each one with who and when. Mix excerpts and quotes freely.
// Put more than one <div class="spread"> in a dialog and the book gets pages to turn: arrows under
// the cover, a click on the right or left page, or the arrow keys. Keep each page to a passage or two.
// On a phone (700px and under) the book shows one page at a time, turned by a tap on the page or the arrows.
//
// The cover, paper and ink colours are fixed: it is a physical book, in the light theme and the dark one.
(function() {
  var font = document.createElement('link');
  font.rel = 'stylesheet';
  font.href = 'https://fonts.googleapis.com/css2?family=Special+Elite&display=swap';
  document.head.appendChild(font);

  var LINE = 30;   // line height, px
  var B = 'dialog.modal.blv-book';
  var css = document.createElement('style');
  css.textContent = [
    // the cover: brown leather showing all round the open pages
    B + '{width:min(960px,95vw);padding:18px 20px 22px;border:0;border-radius:12px;color:#2b3050;',
    'background:radial-gradient(140% 120% at 20% 0%,#7a4f2e 0%,#5b3820 45%,#3f2513 100%);',
    'box-shadow:0 22px 60px rgba(0,0,0,.5),inset 0 0 0 1px rgba(255,220,170,.18),inset 0 0 0 5px rgba(0,0,0,.14),inset 0 0 0 6px rgba(255,220,170,.10);}',
    // the open pages, with the edges of the page block showing beneath
    B + ' .spread{position:relative;display:grid;grid-template-columns:1fr 1fr;border-radius:3px;',
    'box-shadow:0 1px 0 #dcc895,0 3px 0 #bfa56d,0 5px 0 #dcc895,0 7px 0 #a98d55,0 10px 14px rgba(0,0,0,.35);}',
    // the gutter where the pages meet the spine
    B + ' .spread::after{content:"";position:absolute;top:0;bottom:0;left:50%;width:2px;margin-left:-1px;background:rgba(60,38,12,.45);}',
    B + ' .page{position:relative;padding:' + (LINE * 1.5) + 'px 34px ' + LINE + 'px 38px;min-height:' + (LINE * 11) + 'px;}',
    // aged paper: yellowed, darker toward the edges, with a few foxing spots and a water stain
    B + ' .page{box-shadow:inset 0 0 46px rgba(122,84,28,.34),inset 0 0 8px rgba(92,60,18,.30);}',
    B + ' .page.left{border-radius:3px 0 0 3px;background:',
    'linear-gradient(to left,rgba(60,36,8,.38) 0,rgba(60,36,8,.12) 24px,transparent 64px),',
    'radial-gradient(circle at 14% 22%,rgba(140,92,34,.20) 0,rgba(140,92,34,.10) 5px,transparent 11px),',
    'radial-gradient(circle at 72% 64%,rgba(140,92,34,.16) 0,transparent 9px),',
    'radial-gradient(circle at 34% 88%,rgba(140,92,34,.18) 0,transparent 7px),',
    'radial-gradient(60% 34% at 8% 96%,rgba(150,104,44,.22) 0,rgba(150,104,44,.10) 55%,transparent 72%),',
    'radial-gradient(130% 110% at 30% 10%,#f0e2bb 0%,#e4d0a0 55%,#cfb47c 100%);}',
    B + ' .page.right{border-radius:0 3px 3px 0;background:',
    'linear-gradient(to right,rgba(60,36,8,.38) 0,rgba(60,36,8,.12) 24px,transparent 64px),',
    'radial-gradient(circle at 82% 16%,rgba(140,92,34,.18) 0,rgba(140,92,34,.08) 6px,transparent 12px),',
    'radial-gradient(circle at 26% 74%,rgba(140,92,34,.16) 0,transparent 8px),',
    'radial-gradient(circle at 64% 92%,rgba(140,92,34,.15) 0,transparent 6px),',
    'radial-gradient(50% 30% at 94% 4%,rgba(150,104,44,.20) 0,rgba(150,104,44,.08) 55%,transparent 72%),',
    'radial-gradient(130% 110% at 70% 10%,#f0e2bb 0%,#e4d0a0 55%,#cfb47c 100%);}',
    B + ' .head{margin:0 0 ' + LINE + 'px;font-family:Georgia,"Times New Roman",serif;font-size:11.5px;line-height:' + LINE + 'px;letter-spacing:.16em;text-transform:uppercase;color:#7d6238;}',
    B + ' blockquote{margin:0 0 ' + LINE + 'px;padding:0;border:0;background:none;}',
    B + ' blockquote:last-child{margin-bottom:0;}',
    B + ' blockquote p{margin:0;font-family:"Special Elite","American Typewriter","Courier Prime","Courier New",monospace;font-style:normal;font-weight:400;font-size:16.5px;letter-spacing:.01em;line-height:' + LINE + 'px;color:#2e2620;}',
    // passages are shown as they are: no wrapping quotation marks, no ellipses
    B + ' cite{display:block;text-align:right;font-family:Georgia,"Times New Roman",serif;font-style:italic;font-size:14px;line-height:' + LINE + 'px;color:#7d6238;}',
    B + ' cite::before{content:"\\2014\\00a0";}',
    // the close mark floats above the book, outside the cover
    B + '{overflow:visible;max-height:none;}',
    B + ' .spread{max-height:calc(94vh - 110px);overflow:auto;}',
    B + ' .modal-close{top:-40px;right:-6px;font-size:28px;color:#fff;opacity:.85;}',
    B + ' .modal-close:hover{color:#fff;opacity:1;}',
    // several spreads: stacked in one grid cell so the book keeps the size of its fullest spread
    B + ' .leaves{display:grid;perspective:2200px;}',
    B + ' .leaves>.spread{grid-area:1/1;}',
    B + ' .leaves>.spread.off{visibility:hidden;}',
    B + ' .leaves .page{backface-visibility:hidden;-webkit-backface-visibility:hidden;}',
    B + ' .leaves .page.turn{cursor:pointer;}',
    // a turned-up corner on a page that has another behind it
    B + ' .leaves .page.turn.right::after,' + B + ' .leaves .page.turn.left::after{content:"";position:absolute;bottom:0;width:0;height:0;border-style:solid;opacity:.9;}',
    B + ' .leaves .page.turn.right::after{right:0;border-width:0 0 24px 24px;border-color:transparent transparent #5b3820 #c9ad74;}',
    B + ' .leaves .page.turn.left::after{left:0;border-width:0 24px 24px 0;border-color:transparent #c9ad74 #5b3820 transparent;}',
    // page arrows and the page count, under the cover
    B + ' .nav{position:absolute;left:0;right:0;bottom:-46px;display:flex;justify-content:center;align-items:center;gap:16px;color:#fff;font:13px/1 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;font-variant-numeric:tabular-nums;}',
    B + ' .nav button{border:0;background:none;color:#fff;font-size:26px;line-height:1;padding:4px 10px;cursor:pointer;opacity:.85;}',
    B + ' .nav button:hover{opacity:1;}',
    B + ' .nav button:disabled{opacity:.25;cursor:default;}',
    // a book with a single spread has nothing to turn on a wide screen
    B + ' .nav.single{display:none;}',
    // On a narrow screen the book shows one page at a time. Both pages of a spread sit in the same grid
    // cell, so the book keeps the height of its fullest page, and the one not being read is hidden.
    '@media (max-width:700px){' + B + '{width:min(430px,92vw);padding:10px 10px 14px;}' +
      B + ' .spread{grid-template-columns:1fr;max-height:calc(100vh - 150px);max-height:calc(100dvh - 150px);}' +
      B + ' .spread::after{display:none;}' +
      B + ' .spread>.page{grid-area:1/1;border-radius:3px;min-height:' + (LINE * 9) + 'px;padding:' + LINE + 'px 22px ' + (LINE * 1.2) + 'px 26px;}' +
      B + ' .spread[data-side=left]>.page.right,' + B + ' .spread[data-side=right]>.page.left{visibility:hidden;}' +
      // the page being read always has the spine on its left and its turn-up corner at bottom right
      B + ' .page.right{background:' +
        'linear-gradient(to right,rgba(60,36,8,.38) 0,rgba(60,36,8,.12) 18px,transparent 48px),' +
        'radial-gradient(circle at 82% 16%,rgba(140,92,34,.18) 0,rgba(140,92,34,.08) 6px,transparent 12px),' +
        'radial-gradient(circle at 26% 74%,rgba(140,92,34,.16) 0,transparent 8px),' +
        'radial-gradient(130% 110% at 70% 10%,#f0e2bb 0%,#e4d0a0 55%,#cfb47c 100%);}' +
      B + ' .page.left{background:' +
        'linear-gradient(to right,rgba(60,36,8,.38) 0,rgba(60,36,8,.12) 18px,transparent 48px),' +
        'radial-gradient(circle at 14% 22%,rgba(140,92,34,.20) 0,rgba(140,92,34,.10) 5px,transparent 11px),' +
        'radial-gradient(circle at 72% 64%,rgba(140,92,34,.16) 0,transparent 9px),' +
        'radial-gradient(130% 110% at 30% 10%,#f0e2bb 0%,#e4d0a0 55%,#cfb47c 100%);}' +
      B + ' .leaves .page.turn.left::after{left:auto;right:0;border-width:0 0 24px 24px;border-color:transparent transparent #5b3820 #c9ad74;}' +
      B + ' .page.shown{animation:blv-leaf .22s ease-out;}' +
      B + ' .nav.single{display:flex;}' +
      B + ' .nav{bottom:-48px;}' + B + ' .nav button{font-size:30px;padding:6px 18px;}' +
      B + ' blockquote p{font-size:15.5px;}}',
    '@keyframes blv-leaf{from{opacity:0;transform:translateX(10px);}to{opacity:1;transform:none;}}',
    '@media (prefers-reduced-motion:reduce){' + B + ' .page.shown{animation:none;}}'
  ].join('');
  document.head.appendChild(css);

  // Page turning, for any book with more than one spread.
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function setUp(dlg) {
    var spreads = Array.prototype.slice.call(dlg.querySelectorAll(':scope > .spread'));
    if (!spreads.length) return;
    var leaves = document.createElement('div'); leaves.className = 'leaves';
    dlg.insertBefore(leaves, spreads[0]);
    spreads.forEach(function(sp) { leaves.appendChild(sp); });
    var nav = document.createElement('div'); nav.className = 'nav' + (spreads.length < 2 ? ' single' : '');
    var prev = document.createElement('button'); prev.type = 'button'; prev.innerHTML = '&#8249;'; prev.setAttribute('aria-label', 'Previous pages');
    var count = document.createElement('span');
    var next = document.createElement('button'); next.type = 'button'; next.innerHTML = '&#8250;'; next.setAttribute('aria-label', 'Next pages');
    nav.appendChild(prev); nav.appendChild(count); nav.appendChild(next); dlg.appendChild(nav);

    var at = 0, busy = false, HALF = 260;
    // On a phone the unit is a page, not a spread: side says which page of the current spread is showing.
    var side = 'left';
    var mq = window.matchMedia ? window.matchMedia('(max-width:700px)') : { matches: false };
    function narrow() { return mq.matches; }
    function leaf() { return at * 2 + (side === 'right' ? 1 : 0); }
    function page(sp, side) { return sp.querySelector('.page.' + side); }
    function show() {
      spreads.forEach(function(sp, i) {
        sp.classList.toggle('off', i !== at);
        sp.style.zIndex = '';
        sp.setAttribute('data-side', side);
        if (narrow()) {
          // a tap on the page being read turns to the next one
          var more = leaf() < spreads.length * 2 - 1;
          ['left', 'right'].forEach(function(sd) {
            var here = i === at && sd === side;
            page(sp, sd).classList.toggle('turn', here && more);
            page(sp, sd).classList.toggle('shown', here);
          });
        } else {
          page(sp, 'right').classList.toggle('turn', i === at && at < spreads.length - 1);
          page(sp, 'left').classList.toggle('turn', i === at && at > 0);
          page(sp, 'left').classList.remove('shown'); page(sp, 'right').classList.remove('shown');
        }
        ['left', 'right'].forEach(function(side) { var pg = page(sp, side); pg.style.transition = ''; pg.style.transform = ''; pg.style.transformOrigin = ''; });
      });
      if (narrow()) {
        count.textContent = (leaf() + 1) + ' / ' + (spreads.length * 2);
        prev.disabled = leaf() === 0; next.disabled = leaf() === spreads.length * 2 - 1;
      } else {
        count.textContent = (at + 1) + ' / ' + spreads.length;
        prev.disabled = at === 0; next.disabled = at === spreads.length - 1;
      }
    }
    // A turn in two halves. Going forward: the right-hand page lifts and folds up to the spine,
    // uncovering the next right-hand page; then the next left-hand page comes down over the old one.
    function go(dir) {
      if (narrow()) {   // one page forward or back, no fold
        var n = leaf() + dir;
        if (n < 0 || n > spreads.length * 2 - 1) return;
        at = Math.floor(n / 2); side = n % 2 ? 'right' : 'left';
        show();
        spreads[at].scrollTop = 0;
        return;
      }
      var to = at + dir;
      if (busy || to < 0 || to >= spreads.length) return;
      if (reduced) { at = to; show(); return; }
      busy = true;
      var from = spreads[at], dest = spreads[to];
      var lift = dir > 0 ? 'right' : 'left', land = dir > 0 ? 'left' : 'right';
      var out = page(from, lift), inn = page(dest, land);
      dest.classList.remove('off'); dest.style.zIndex = 1; from.style.zIndex = 2;
      inn.style.transform = 'rotateY(' + (dir > 0 ? 90 : -90) + 'deg)';
      inn.style.transformOrigin = dir > 0 ? '100% 50%' : '0 50%';
      out.style.transformOrigin = dir > 0 ? '0 50%' : '100% 50%';
      out.style.transition = 'transform ' + HALF + 'ms ease-in';
      requestAnimationFrame(function() { out.style.transform = 'rotateY(' + (dir > 0 ? -90 : 90) + 'deg)'; });
      setTimeout(function() {
        dest.style.zIndex = 3;
        inn.style.transition = 'transform ' + HALF + 'ms ease-out';
        requestAnimationFrame(function() { inn.style.transform = 'rotateY(0deg)'; });
        setTimeout(function() { at = to; busy = false; show(); }, HALF + 30);
      }, HALF + 20);
    }
    prev.addEventListener('click', function() { go(-1); });
    next.addEventListener('click', function() { go(1); });
    leaves.addEventListener('click', function(e) {
      var pg = e.target.closest && e.target.closest('.page.turn');
      if (pg) go(narrow() || pg.classList.contains('right') ? 1 : -1);
    });
    dlg.addEventListener('keydown', function(e) {
      if (e.key === 'ArrowRight') go(1); else if (e.key === 'ArrowLeft') go(-1);
    });
    dlg.addEventListener('modal:open', function() { at = 0; side = 'left'; busy = false; show(); });   // always open at the first pages
    // rotating the phone or resizing the window switches between pages and spreads
    var onSize = function() { side = 'left'; busy = false; show(); };
    if (mq.addEventListener) mq.addEventListener('change', onSize); else if (mq.addListener) mq.addListener(onSize);
    show();
  }
  function init() { Array.prototype.forEach.call(document.querySelectorAll('dialog.blv-book'), setUp); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
