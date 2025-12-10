document.addEventListener("click", (e) => {
  const dot = e.target.closest(".menu-dot");
  const menu = e.target.closest(".song-menu");

  document.querySelectorAll(".song-menu.open").forEach(m => {
    if (m !== menu) m.classList.remove("open");
  });

  if (dot && menu) {
    menu.classList.toggle("open");
    e.preventDefault();
    return;
  }

  if (!e.target.closest(".menu-dropdown")) {
    document.querySelectorAll(".song-menu.open").forEach(m => m.classList.remove("open"));
  }
});

document.addEventListener("click", (e) => {
  const btn = e.target.closest("[data-edit-note]");
  if (!btn) return;

  const songId = btn.getAttribute("data-song-id");
  const current = btn.getAttribute("data-current-note") || "";

  const updated = window.prompt("Edit your note", current);
  if (updated === null) return;

  const scope = btn.closest(".song-right, .overview-actions, .mood-overview-item, .song-item");
  if (!scope) return;

  const form = scope.querySelector(".note-update-form");
  if (!form) return;

  const noteInput = form.querySelector("input[name='note']");
  noteInput.value = updated.trim();

  form.submit();
});
