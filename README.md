# OpenCode Gateway UI preview

Dependency-free Arabic/English, RTL/LTR frontend. Run:

```bash
python3 -m http.server 3000 --bind 0.0.0.0
```

Open http://localhost:3000. The landing page has no sidebar; the workspace has a compact sessions sidebar, repository/branch preview selectors, prompt preview, Files/Diff/Logs, and review controls. Light/dark mode and language preferences persist locally.

## Integration status

This branch is a design prototype. Login/register open the workspace preview and discard form inputs; they do not authenticate or save credentials. GitHub OAuth, repository/branch APIs, OpenCode execution, account/trial/billing services and live metrics are not implemented. Repository selections are examples. Commit and Push stay disabled until backend integration; prompt messages explicitly report that no commands were executed. The 10-day offer is marketing copy, not an active trial service.

The only Yemen illustration is the local hero SVG; authentication uses a coding terminal illustration instead. Assets work without external image/CDN dependencies. config.js retains the existing OpenCode endpoint for future integration.
