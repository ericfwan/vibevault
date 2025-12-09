function stopAllAudio(exceptAudio = null) {
  document.querySelectorAll("audio[data-vv-audio]").forEach(a => {
    if (exceptAudio && a === exceptAudio) return;
    a.pause();
    a.currentTime = 0;
  });
}

function resetAllToggleButtons(exceptBtn = null) {
  document.querySelectorAll("[data-audio-toggle]").forEach(btn => {
    if (exceptBtn && btn === exceptBtn) return;
    btn.textContent = "Play";
  });
}

function getOrCreateAudio(container, url) {
  let audio = container.querySelector("audio[data-vv-audio]");
  if (!audio) {
    audio = document.createElement("audio");
    audio.setAttribute("data-vv-audio", "1");
    audio.src = url;
    container.appendChild(audio);
  } else if (audio.src !== url) {
    audio.src = url;
  }
  return audio;
}

document.addEventListener("click", (e) => {
  const toggleBtn = e.target.closest("[data-audio-toggle]");
  if (!toggleBtn) return;

  const container = toggleBtn.closest("[data-preview-url]");
  if (!container) return;

  const url = container.dataset.previewUrl || "";
  if (!url) return;

  const audio = getOrCreateAudio(container, url);

  if (audio.paused) {
    stopAllAudio(audio);
    resetAllToggleButtons(toggleBtn);
    audio.play().catch(() => {});
    toggleBtn.textContent = "Pause";
  } else {
    audio.pause();
    toggleBtn.textContent = "Play";
  }

  audio.onended = () => {
    toggleBtn.textContent = "Play";
  };

  audio.onpause = () => {
    if (audio.currentTime === 0 || audio.ended) {
      toggleBtn.textContent = "Play";
    }
  };
});

document.addEventListener("DOMContentLoaded", () => {
  const highlighted = document.querySelector(".song-item.highlight");
  if (highlighted) {
    highlighted.scrollIntoView({ behavior: "smooth", block: "center" });
  }
});
