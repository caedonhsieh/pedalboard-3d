/* Shared hero switcher: a dropdown in every hero page's control bar that
 * jumps to another finished hero. The pedal list is the ledger's hero set;
 * add a line here when a new hero ships. Navigation is a plain page load, so
 * the switcher needs no state from the page it runs on. */
(function () {
  var HEROES = [
    ['mxr-phase90.html', 'MXR Phase 90'],
    ['boss-ds1.html', 'Boss DS-1'],
    ['boss-sd1.html', 'Boss SD-1'],
    ['boss-dd8.html', 'Boss DD-8'],
    ['boss-ce2w.html', 'Boss CE-2W'],
    ['boss-tu3.html', 'Boss TU-3'],
    ['ibanez-ts9.html', 'Ibanez TS9'],
    ['mxr-dyna-comp.html', 'MXR Dyna Comp'],
    ['mxr-carbon-copy.html', 'MXR Carbon Copy'],
    ['ehx-big-muff-pi.html', 'EHX Big Muff Pi'],
    ['ehx-small-clone.html', 'EHX Small Clone'],
    ['ehx-deluxe-memory-man.html', 'EHX Deluxe Memory Man'],
    ['proco-rat2.html', 'ProCo Rat 2'],
    ['fulltone-ocd.html', 'Fulltone OCD'],
    ['klon-centaur.html', 'Klon Centaur'],
    ['xotic-ep-booster.html', 'Xotic EP Booster'],
    ['tc-electronic-ditto.html', 'TC Electronic Ditto'],
    ['tc-electronic-hall-of-fame-2.html', 'TC Hall of Fame 2'],
    ['strymon-timeline.html', 'Strymon TimeLine'],
    ['strymon-bigsky.html', 'Strymon BigSky'],
    ['dunlop-crybaby-gcb95.html', 'Dunlop Cry Baby GCB95'],
    ['dunlop-fuzz-face.html', 'Dunlop Fuzz Face']
  ];
  var bar = document.getElementById('controls');
  if (!bar) return;
  var here = location.pathname.split('/').pop();
  var sel = document.createElement('select');
  sel.id = 'hero-switcher';
  sel.setAttribute('aria-label', 'Switch hero pedal');
  sel.title = 'Switch hero pedal';
  for (var i = 0; i < HEROES.length; i++) {
    var opt = document.createElement('option');
    opt.value = HEROES[i][0];
    opt.textContent = HEROES[i][1];
    if (HEROES[i][0] === here) opt.selected = true;
    sel.appendChild(opt);
  }
  sel.style.cssText = 'pointer-events:auto;background:rgba(22,22,26,.92);color:#e8e9ec;' +
    'border:1px solid #2b2b33;border-radius:999px;padding:8px 10px;font:600 12.5px system-ui;' +
    'max-width:190px;cursor:pointer;';
  sel.addEventListener('change', function () {
    if (sel.value && sel.value !== here) location.href = './' + sel.value;
  });
  // Keep the switcher out of the page's own pointer handling on the canvas bar.
  sel.addEventListener('pointerdown', function (e) { e.stopPropagation(); });
  bar.insertBefore(sel, bar.firstChild);
})();
