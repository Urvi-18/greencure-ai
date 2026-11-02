const BRAND = "AgriCure AI";
const PAGES = [
  { href: "index.html", label: "🔍 Scan & Detect" },
  { href: "blog.html", label: "📖 Plant Care Blog" },
  { href: "game.html", label: "🎮 Mini Game" },
];
const PEOPLE = [
  { name: "Urvi Pal", links: [
    ["Email", "mailto:urvipal106@gmail.com"],
    ["GitHub", "https://github.com/Urvi-18/"],
    ["LinkedIn", "https://www.linkedin.com/in/urvipal18"],
  ]},
  { name: "Vindhya Raj", links: [
    ["Email", "mailto:vindhyaraj98522@gmail.com"],
    ["GitHub", "https://github.com/Vindhya110603"],
    ["LinkedIn", "https://www.linkedin.com/in/vindhya-raj-b4b400301"],
  ]},
];

(function () {
  const here = location.pathname.split("/").pop() || "index.html";
  const nav = PAGES.map(p =>
    `<a href="${p.href}" class="${here === p.href ? "active" : ""}">${p.label}</a>`).join("");

  document.getElementById("site-header").innerHTML = `
    <div class="container">
      <a class="brand" href="index.html">
        <div class="brand-logo">🌿</div>
        <div><div class="brand-name">${BRAND}</div><div class="brand-sub">Leaf health scanner</div></div>
      </a>
      <nav class="nav">${nav}</nav>
    </div>`;

  const people = PEOPLE.map(p => `
    <div class="person"><b>${p.name}</b><div class="links">
      ${p.links.map(([t, u]) => `<a href="${u}" target="_blank" rel="noopener noreferrer">${t}</a>`).join("")}
    </div></div>`).join("");

  document.getElementById("site-footer").innerHTML = `
    <div class="container">
      <div class="footer-top">
        <div>
          <div class="footer-brand">🌿 ${BRAND}</div>
          <div>Created &amp; maintained by <b style="color:#fff">Urvi Pal</b> &amp; <b style="color:#fff">Vindhya Raj</b></div>
        </div>
        <div class="people">${people}</div>
      </div>
      <div class="footer-bottom">© 2026 ${BRAND}. Works on mobile, tablet and desktop.</div>
    </div>`;
})();