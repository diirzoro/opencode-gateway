const cfg = window.OPENCODE_CONFIG || {};
const state = {
  openCodeUrl: localStorage.getItem("openCodeUrl") || cfg.openCodeUrl || "http://127.0.0.1:4096"
};

const $ = (id) => document.getElementById(id);
const toast = (msg) => {
  const el = $("toast");
  el.textContent = msg;
  el.classList.add("show");
  setTimeout(() => el.classList.remove("show"), 2200);
};

document.querySelectorAll(".nav-item").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".nav-item").forEach(x => x.classList.remove("active"));
    document.querySelectorAll(".view").forEach(x => x.classList.remove("active"));
    btn.classList.add("active");
    $(btn.dataset.view).classList.add("active");
    $("pageTitle").textContent = btn.querySelector("span").textContent;
    $("pageSubtitle").textContent =
      btn.dataset.view === "dashboard" ? "Start coding from anywhere." :
      btn.dataset.view === "projects" ? "Connect and open your repositories." :
      btn.dataset.view === "providers" ? "Bring your own AI provider." :
      "Manage the lightweight gateway.";
  });
});

function launchOpenCode() {
  window.open(state.openCodeUrl, "_blank", "noopener");
}
["launchOpenCode","launchProject","openProviders"].forEach(id => $(id).addEventListener("click", launchOpenCode));

["connectGithub","connectGithub2"].forEach(id => $(id).addEventListener("click", () => {
  toast("GitHub OAuth will be connected in the next step.");
}));

$("serverUrl").value = state.openCodeUrl;
$("saveSettings").addEventListener("click", () => {
  state.openCodeUrl = $("serverUrl").value.trim();
  localStorage.setItem("openCodeUrl", state.openCodeUrl);
  toast("Gateway settings saved in this browser.");
});

$("saveAd").addEventListener("click", () => {
  $("adTitle").textContent = $("adminAdTitle").value;
  $("adText").textContent = $("adminAdText").value;
  $("adLink").href = $("adminAdLink").value || "#";
  localStorage.setItem("adTitle", $("adminAdTitle").value);
  localStorage.setItem("adText", $("adminAdText").value);
  localStorage.setItem("adLink", $("adminAdLink").value);
  toast("Ad updated.");
});

const savedAdTitle = localStorage.getItem("adTitle");
const savedAdText = localStorage.getItem("adText");
const savedAdLink = localStorage.getItem("adLink");
if (savedAdTitle) $("adTitle").textContent = $("adminAdTitle").value = savedAdTitle;
if (savedAdText) $("adText").textContent = $("adminAdText").value = savedAdText;
if (savedAdLink) $("adLink").href = $("adminAdLink").value = savedAdLink;

$("themeToggle").addEventListener("click", () => {
  document.documentElement.classList.toggle("light");
  $("themeToggle").textContent = document.documentElement.classList.contains("light") ? "☀" : "☾";
});

async function checkServer() {
  // Cross-origin responses may be blocked before CORS is configured,
  // so this is a friendly visual indicator rather than a hard health check.
  try {
    await fetch(state.openCodeUrl, { mode: "no-cors", cache: "no-store" });
    $("serverStatus").textContent = "Server reachable";
  } catch {
    $("serverStatus").textContent = "Server status unknown";
  }
}
checkServer();
