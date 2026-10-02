# OpenCode Gateway

**Hosted OpenCode. Your GitHub. Your AI.**

This repository contains the lightweight Arabic/English frontend and the Phase 1
FastAPI account service. Accounts, sessions, customer profiles, locations, trial
state, and admin user listing are database-backed. GitHub, OpenCode, workspaces,
billing, and payment actions remain clearly simulated.

## Phase 1 stack

- Static HTML, CSS, and JavaScript frontend
- FastAPI API
- PostgreSQL
- SQLAlchemy 2
- Alembic migrations
- Scrypt password hashing and hashed opaque session tokens

## Run locally

1. Create the environment and PostgreSQL database:

```bash
cp .env.example .env
# Export values from .env in your shell, then:
docker compose up -d postgres
python3 -m venv .venv
. .venv/bin/activate
pip install -r backend/requirements.txt
```

2. Apply migration `0001_accounts` and start the same-origin frontend/API server:

```bash
cd backend
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open <http://localhost:8000>. Do not use the old standalone Python static server
for real account flows because it cannot serve the `/api` endpoints.

## Environment variables

| Variable | Purpose |
| --- | --- |
| `DATABASE_URL` | SQLAlchemy PostgreSQL URL; required in production |
| `SESSION_COOKIE_NAME` | Cookie name; defaults to `gateway_session` |
| `SESSION_DAYS` | Session lifetime; defaults to 14 days |
| `COOKIE_SECURE` | Set `true` behind production HTTPS |

Never commit production database passwords or secrets. The raw session token is
sent only in an HttpOnly, SameSite=Strict cookie; PostgreSQL stores its SHA-256
hash. Passwords are salted and hashed with scrypt.

## API

```text
POST  /api/auth/register
POST  /api/auth/login
POST  /api/auth/logout
GET   /api/auth/me
GET   /api/profile
PATCH /api/profile
GET   /api/locations/countries
GET   /api/locations/countries/{id}/regions
GET   /api/locations/regions/{id}/cities
GET   /api/admin/users                 (admin only)
GET   /api/health
```

## Database schema

Migration `backend/alembic/versions/0001_accounts_and_locations.py` creates:

- `users`: identity, hashed password, contact/location references, role/status,
  preferences, trial timestamps, last login, and audit timestamps.
- `auth_sessions`: user, hashed token, expiry, last seen, revocation, and creation.
- `countries`, `regions`, and `cities`: enabled location hierarchy.

Repository source code is never stored in PostgreSQL. GitHub remains the intended
permanent source of truth.

## Manual acceptance flow

1. Start PostgreSQL, apply migrations, and run Uvicorn.
2. Open **Connect GitHub**, choose **Create account**, and fill every required field.
3. Confirm registration opens the customer account with database-backed profile
   and 10-day trial values.
4. Log out, then log in with either username or email.
5. Open Account and confirm profile/location/trial data is loaded from `/api/profile`.
6. Promote a trusted existing account with `cd backend && python -m scripts.promote_admin owner@example.com`, log in again, open Admin, and confirm `/api/admin/users` lists registered accounts.
7. Inspect PostgreSQL if desired: `psql "$DATABASE_URL" -c 'select username,email,role,trial_ends_at from users;'`.

## Functionality status

| Capability | Status |
| --- | --- |
| Registration, login, logout, sessions | Real / database-backed |
| Customer profile and trial state | Real / database-backed |
| Country, region, and city lookup | Real / database-backed |
| Admin authentication and user listing | Real / role-protected |
| GitHub connection and repository/branch loading | Simulated |
| Temporary workspace and OpenCode agent | Simulated |
| Files, Diff, Logs, Commit, and Push | Sample/simulated |
| Plans, PayPal, bank transfer, receipts | UI-only |
| Subscription enforcement and financial reporting | Not implemented |
| Password reset and email verification | Not implemented |

## Tests

```bash
cd backend
pytest -q
```

The test suite covers registration, validation, duplicate prevention, cookie
sessions, logout/re-login, profile loading, location lookup, admin authorization,
and password hashing.

## Production deployment

The production process binds to `127.0.0.1:8000`, uses the VPS PostgreSQL service,
and is managed by systemd. OpenCode remains separate on port `4096` and is not
integrated in this phase. See [`deployment/README.md`](deployment/README.md) for
exact Ubuntu 24.04 PostgreSQL, virtualenv, migration, permissions, systemd,
update, and health-check commands. The service template is
[`deployment/opencode-gateway.service`](deployment/opencode-gateway.service).
