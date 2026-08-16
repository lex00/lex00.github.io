// Music toggle.
//
// Off by default and silent until someone clicks it. Browsers block autoplay
// with sound anyway, so there is no version of this that starts on its own.
// The choice is remembered across pages in localStorage, and the control only
// renders when the layout found an audio file to point at.

(function () {
  var KEY = 'lex00:music';
  var btn = document.querySelector('[data-music-src]');
  if (!btn) return;

  var audio = new Audio(btn.dataset.musicSrc);
  audio.loop = true;
  audio.volume = 0.35;
  audio.preload = 'none';

  function paint(on) {
    btn.setAttribute('aria-pressed', on ? 'true' : 'false');
    btn.setAttribute('aria-label', on ? 'Stop music' : 'Play music');
    btn.classList.toggle('is-playing', on);
  }

  function stop() {
    audio.pause();
    try { localStorage.setItem(KEY, 'off'); } catch (e) {}
    paint(false);
  }

  function play() {
    // A rejected promise means the browser refused. Stay honest about state.
    var p = audio.play();
    if (p && p.catch) {
      p.then(function () {
        try { localStorage.setItem(KEY, 'on'); } catch (e) {}
        paint(true);
      }).catch(function () {
        paint(false);
      });
    } else {
      paint(true);
    }
  }

  btn.addEventListener('click', function () {
    if (audio.paused) play(); else stop();
  });

  paint(false);

  // Carry the choice across a navigation, but only because a click set it
  // earlier. The first gesture on the new page is what unlocks playback.
  var saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) {}
  if (saved === 'on') {
    var resume = function () {
      document.removeEventListener('pointerdown', resume);
      document.removeEventListener('keydown', resume);
      play();
    };
    document.addEventListener('pointerdown', resume, { once: true });
    document.addEventListener('keydown', resume, { once: true });
  }
})();
