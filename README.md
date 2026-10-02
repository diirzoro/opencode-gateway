# OpenCode Gateway MVP

A tiny, dependency-free frontend for your hosted OpenCode experiment.

## What is included now

- Attractive responsive dashboard
- User navigation
- Madarasati quick-launch card
- OpenCode launch button
- AI provider section that deliberately delegates provider setup to OpenCode
- Small Admin page
- Editable ad slot
- Editable OpenCode URL
- Dark/light UI
- No npm dependencies and almost no server resource usage

## What is intentionally NOT implemented yet

- Real GitHub OAuth
- Repository / branch API
- User authentication
- PostgreSQL persistence
- Billing
- Per-user Docker isolation

Those should be added only after the owner workflow is proven.

## Run on the VPS

From this folder:

```bash
python3 -m http.server 3000 --bind 0.0.0.0
```

Then open:

`http://YOUR_SERVER_IP:3000`

OpenCode remains on port 4096.

## Change OpenCode URL

Edit `config.js`, or use Admin -> Gateway settings in the browser.

## Recommended next step

Implement GitHub OAuth + repository/branch selection, then test only with your own GitHub and Madarasati before adding public users.
