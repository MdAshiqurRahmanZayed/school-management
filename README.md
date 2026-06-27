# School Management — Odoo 16

Custom Odoo 16 module for school operations. Runs via Docker Compose.

---

## Prerequisites

- Docker + Docker Compose installed
- PostgreSQL running (external — not in Docker Compose)
- Fill in DB credentials in `config/odoo.conf` before first run

---

## Project structure

```
school-management/
├── docker-compose.yml
├── config/odoo.conf          ← DB connection config
├── addons/                   ← our modules (git tracked)
│   ├── school_management/
│   └── school_user_management/
└── extra-addons/             ← OCA modules (gitignored, clone manually)
    ├── web_responsive/
    └── base_user_role/
```

---

## First-time setup

### 1. Clone OCA modules

```bash
git clone --branch 16.0 --depth 1 https://github.com/OCA/web.git /tmp/oca_web
cp -r /tmp/oca_web/web_responsive ./extra-addons/
cp -r ~/Desktop/Projects/erp/erp-odoo/docker-addons/server-backend/base_user_role ./extra-addons/
```

### 2. Configure DB

Edit `config/odoo.conf`:

```ini
db_host = host.docker.internal
db_port = 5432
db_user = your_db_user
db_password = your_db_password
db_name = your_db_name
```

### 3. Install modules

```bash
docker-compose run --rm odoo odoo -i web_responsive,base_user_role,school_management,school_user_management -d your_db_name --stop-after-init
```

---

## Daily commands

### Start — foreground (logs visible)

```bash
docker-compose up
```

`Ctrl+C` to stop.

### Start — background

```bash
docker-compose up -d
```

### Stop

```bash
docker-compose down
```

---

## After code changes

### Upgrade + start with live logs

```bash
docker-compose run --rm odoo odoo -u school_management,school_user_management -d your_db_name --stop-after-init && docker-compose up
```

### Upgrade only (no server start)

```bash
docker-compose run --rm odoo odoo -u school_management,school_user_management -d your_db_name --stop-after-init
```

### Upgrade single module

```bash
docker-compose run --rm odoo odoo -u school_user_management -d your_db_name --stop-after-init
```

---

## Logs

```bash
docker-compose logs -f odoo                  # live follow
docker-compose logs --tail=50 odoo           # last 50 lines
docker logs school-management-odoo-1         # stopped container
```

---

## Open in browser

| URL | Purpose |
|-----|---------|
| `http://localhost:8069` | Normal |
| `http://localhost:8069/web?debug=1` | Dev mode (technical menu, field names) |

---

## Installed modules

| Module | Purpose |
|--------|---------|
| `web_responsive` | Hamburger menu, mobile-friendly UI |
| `base_user_role` | Dynamic role engine (`res.users.role`) |
| `school_management` | Core school module — groups, models, views |
| `school_user_management` | Role & user management app |

Install order: `web_responsive → base_user_role → school_management → school_user_management`

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `service "odoo" is not running` | Use `docker-compose run --rm` or start with `docker-compose up -d` first |
| `KeyError: 'ir.http'` | DB not initialized — run `-i` install command |
| `External ID not found` | Wrong load order in `__manifest__.py` — actions must load before menus |
| Container keeps restarting | `docker logs school-management-odoo-1` to see crash reason |
| Can't connect to DB | Use `host.docker.internal` as `db_host` if DB runs on Mac host |
