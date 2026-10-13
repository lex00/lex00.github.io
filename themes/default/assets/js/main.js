// The DO NOT PRESS button.
//
// One-shot sound on a deliberate click. Nothing plays on load, nothing loops,
// and browsers would block it anyway without a gesture. The label escalates
// with each press, which is the whole joke.

(function () {
  var btn = document.querySelector('[data-sound-src]');
  if (!btn) return;

  var label = btn.querySelector('.dnp-label');
  var stage = btn.closest('.dnp-stage') || btn;
  var audio = new Audio(btn.dataset.soundSrc);
  audio.preload = 'auto';
  audio.volume = 0.7;

  var lines = [
    'I said do not press',
    'Stop that',
    'This is a resume',
    'You are still pressing',
    'Fine. Hire me',
  ];
  var n = 0;

  btn.addEventListener('click', function () {
    // Rewind so rapid presses retrigger instead of being ignored. Seeking
    // before any data has loaded throws in some browsers, so guard it.
    try { audio.currentTime = 0; } catch (e) {}
    var p = audio.play();
    if (p && p.catch) p.catch(function () {});

    if (label) label.textContent = lines[Math.min(n, lines.length - 1)];
    n++;

    stage.classList.remove('is-firing');
    // Force a reflow so the animation restarts on every press.
    void stage.offsetWidth;
    stage.classList.add('is-firing');
  });

  stage.addEventListener('animationend', function (e) {
    if (e.target === btn) stage.classList.remove('is-firing');
  });
})();

// Copy buttons on agent prompts. Reads the text from the block it sits in,
// so the prompt is written once, in the post.
(function () {
  document.querySelectorAll('[data-copy-target]').forEach(function (btn) {
    var block = btn.closest('.agent-prompt');
    var code = block && block.querySelector('code');
    if (!code || !navigator.clipboard) { btn.hidden = true; return; }
    btn.addEventListener('click', function () {
      navigator.clipboard.writeText(code.textContent).then(function () {
        btn.textContent = 'Copied';
        setTimeout(function () { btn.textContent = 'Copy'; }, 1600);
      }, function () {});
    });
  });
})();
