# OpenCode Gateway visual prototype

**Hosted OpenCode. Your GitHub. Your AI.**

This repository contains a lightweight, dependency-free product prototype for
the complete OpenCode Gateway journey:

```text
Landing → GitHub preview → repository/branch → OpenCode workspace
        → Agent → Files/Diff/Logs → Commit/Push preview
```

The hybrid design uses a clear pipeline on the public and onboarding screens,
a mission-control desktop workspace, and an agent-first mobile workspace.

## Preview locally

```bash
python3 -m http.server 4173
```

Open <http://localhost:4173>. Use **Connect GitHub** for the onboarding flow or
**View workspace** to go directly to the coding workspace.

## Prototype boundaries

- All GitHub, OpenCode, agent, commit, and push behaviors are simulations.
- No form credentials, source files, prompts, or secrets are transmitted.
- Commit and push buttons only display preview feedback.
- Language and theme preferences are the only values stored, using
  `localStorage` in the browser.
- The prototype supports Arabic/RTL, English/LTR, light mode, dark mode, and
  dedicated desktop and mobile workspace layouts.

## Files

- `index.html` — landing, onboarding, and workspace surfaces.
- `styles.css` — visual system, themes, responsive layouts, and mobile sheets.
- `app.js` — localization and simulated prototype interactions.
- `assets/yemen-hero.svg` — the single Yemen/Sana'a visual, used only in the hero.
- `reference/original-prototype/` — snapshot of the previous prototype kept for
  comparison and rollback reference.

No build step or package installation is required.
