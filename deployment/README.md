# Ubuntu 24.04 deployment

The gateway runs on `127.0.0.1:8000`. PostgreSQL uses the VPS system service.
OpenCode remains a separate service on port `4096`; Phase 1 does not connect to it.
Docker Compose is for optional development only.

## 1. Install system packages

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip postgresql-client curl
```

PostgreSQL is already installed, so verify it instead of installing another server:

```bash
sudo systemctl enable --now postgresql
sudo systemctl status postgresql --no-pager
```

## 2. Copy or clone the project

```bash
sudo install -d -o tahir -g tahir -m 0750 /home/tahir/opencode-gateway
sudo install -d -o tahir -g tahir -m 0750 /var/lib/opencode-runtime
sudo install -d -o tahir -g tahir -m 0750 /var/lib/opencode-workspaces
# Copy the approved tree into /home/tahir/opencode-gateway, or:
sudo -u tahir git clone YOUR_REPOSITORY_URL /home/tahir/opencode-gateway
cd /home/tahir/opencode-gateway
```

## 3. Create the PostgreSQL role and database

Generate a long password locally, then use it in both PostgreSQL and `.env`:

```bash
openssl rand -base64 36
sudo -u postgres psql <<'SQL'
CREATE ROLE opencode_gateway LOGIN PASSWORD 'REPLACE_WITH_A_LONG_RANDOM_PASSWORD';
CREATE DATABASE opencode_gateway OWNER opencode_gateway;
REVOKE ALL ON DATABASE opencode_gateway FROM PUBLIC;
\c opencode_gateway
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT USAGE, CREATE ON SCHEMA public TO opencode_gateway;
SQL
```

Do not paste the real password into shell history on a shared server; using `sudo -u
postgres psql` interactively is safer.

## 4. Configure the environment and Python

```bash
cd /home/tahir/opencode-gateway
cp .env.example .env
chmod 0600 .env
chown tahir:tahir .env
nano .env
sudo -u tahir python3 -m venv .venv
sudo -u tahir .venv/bin/python -m pip install --upgrade pip
sudo -u tahir .venv/bin/pip install -r backend/requirements.txt
```

Production values must include:

```ini
DATABASE_URL=postgresql+psycopg://opencode_gateway:URL_ENCODED_PASSWORD@127.0.0.1:5432/opencode_gateway
SESSION_COOKIE_NAME=gateway_session
SESSION_DAYS=14
COOKIE_SECURE=true
APP_HOST=127.0.0.1
APP_PORT=8000
```

Use an HTTPS reverse proxy before enabling public access. `COOKIE_SECURE=true` means
login cookies will only work through HTTPS, not directly over plain HTTP.

## 5. Apply the database migration

```bash
cd /home/tahir/opencode-gateway/backend
set -a; source ../.env; set +a
../.venv/bin/alembic upgrade head
../.venv/bin/alembic current
```

## 6. Install and start systemd

```bash
sudo cp /home/tahir/opencode-gateway/deployment/opencode-gateway.service /etc/systemd/system/opencode-gateway.service
sudo chmod 0644 /etc/systemd/system/opencode-gateway.service
sudo systemctl daemon-reload
sudo systemctl enable --now opencode-gateway
sudo systemctl status opencode-gateway --no-pager
```

Restart after application changes:

```bash
sudo systemctl restart opencode-gateway
sudo journalctl -u opencode-gateway -n 100 --no-pager
```

## 7. Verify health

```bash
curl --fail --silent --show-error http://127.0.0.1:8000/api/health
# Expected: {"status":"ok"}
```

## Updating

```bash
cd /home/tahir/opencode-gateway
sudo -u tahir git pull --ff-only
sudo -u tahir .venv/bin/pip install -r backend/requirements.txt
cd backend
set -a; source ../.env; set +a
../.venv/bin/alembic upgrade head
sudo systemctl restart opencode-gateway
curl --fail http://127.0.0.1:8000/api/health
```

## Permissions and files that must remain private

- Project directories: owner `tahir:tahir`, mode `0750`.
- `.env`: owner `tahir:tahir`, mode `0600`.
- Runtime/workspace directories: owner `tahir:tahir`, mode `0750`.
- Never commit `.env`, private keys, database dumps/files, virtual environments,
  logs, runtime data, workspaces, uploaded receipts, or provider/GitHub credentials.
- `.env.example` contains placeholders only and should remain committed.
