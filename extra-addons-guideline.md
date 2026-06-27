# Extra Addons — OCA Setup Guide

`extra-addons/` folder is **gitignored**. Clone OCA modules here manually after cloning this repo.

---

## Folder purpose

```
extra-addons/    ← gitignored, clone OCA modules here
addons/          ← tracked, our custom modules go here
```

Both are mounted into Docker as separate addon paths.

---

## Required OCA modules

> **Note:** `base_user_role` is NOT available in OCA for Odoo 16.0.
> Role management is handled by our custom `school_user_management` module instead.

| Module | OCA Repo | Branch | Purpose | Status |
|--------|----------|--------|---------|--------|
| `web_responsive` | `OCA/web` | `16.0` | Hamburger menu, mobile-friendly Odoo backend | ✅ cloned |
| `base_user_role` | internal (from erp-odoo project) | `16.0` | `res.users.role` dynamic role model | ✅ copied |

The `extra-addons/` folder holds OCA/third-party modules that are gitignored.

---

## Setup after cloning this repo

Run these commands once from the project root (`school-management/`):

### Step 1 — create the folder

```bash
mkdir -p extra-addons
```

### Step 2 — clone `web_responsive`

```bash
git clone --branch 16.0 --depth 1 https://github.com/OCA/web.git /tmp/oca_web
cp -r /tmp/oca_web/web_responsive ./extra-addons/
```

### Step 3 — verify structure

```
extra-addons/
└── web_responsive/
    ├── __manifest__.py
    ├── __init__.py
    └── ...
```

### Step 4 — start Docker

```bash
docker-compose up -d
```

### Step 5 — install modules in order

```bash
docker-compose exec odoo odoo \
  -i base_user_role,school_management,school_user_management \
  -d odoo --stop-after-init
```

---

## Adding more OCA modules in future

1. Find module in OCA GitHub: `github.com/OCA/<repo>/tree/16.0/<module_name>`
2. Clone/copy into `extra-addons/`
3. Add entry to the table above in this file (commit the guideline update)
4. Restart Odoo and install via Apps menu or `-i <module_name>`

---

## Why gitignore extra-addons?

- OCA modules are maintained by OCA, not us — their git history is irrelevant here
- Large repos with many modules; only need a few
- Each dev clones what they need from OCA directly
- Avoids submodule complexity for a learning project

If this were production, use `git submodule` or `pip install odoo-addon-*` instead.
