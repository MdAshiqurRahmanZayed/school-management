# School Management — Odoo 16 Module

## Project context

Learning project. Goal: build a full Odoo 16 custom module for school management.
User is a Python beginner learning Odoo from scratch.

**Odoo version:** 16
**Type:** Custom addon module
**Purpose:** Learning sandbox — not a production school system

---

## Key Odoo concepts (reference when helping)

### Module structure
Every Odoo module is a Python package inside the `addons` path:
```
school_management/
├── __init__.py          # imports models package
├── __manifest__.py      # module metadata + file list
├── models/
│   ├── __init__.py      # imports each model file
│   └── school_info.py   # one file per model (convention)
├── views/
│   └── school_info_views.xml
├── security/
│   └── ir.model.access.csv   # CRUD permissions per model per group
├── data/                # config/demo XML data
├── wizards/             # TransientModel popups
└── reports/             # QWeb PDF reports
```

### Model types
- `models.Model` — regular persistent record (use for everything here)
- `models.TransientModel` — wizard/popup, auto-deleted after use
- `models.AbstractModel` — mixin, never instantiated directly

### Field types used in this project
| Field | Use |
|-------|-----|
| `fields.Char` | short text |
| `fields.Text` | long text |
| `fields.Integer` | whole number |
| `fields.Float` | decimal |
| `fields.Date` | date only |
| `fields.Datetime` | date + time |
| `fields.Boolean` | true/false |
| `fields.Selection` | dropdown with fixed options |
| `fields.Many2one` | foreign key (N records → 1) |
| `fields.One2many` | reverse of Many2one (1 → N) |
| `fields.Many2many` | N → N relationship |
| `fields.Binary` | file/image upload |
| `fields.Html` | rich text |

### Decorators
- `@api.depends('field1', 'field2')` — recompute computed field when deps change
- `@api.onchange('field')` — react to UI field change (not saved yet)
- `@api.constrains('field')` — validate before save, raise `ValidationError`
- `@api.model` — method has no `self` record, works on model class

### Views
Every view is XML. Four main types:
- `form` — single record edit
- `tree` (list) — multi-record table
- `kanban` — card board
- `search` — filters + group-by panel

### Security (ir.model.access.csv)
Format: `id,name,model_id,group_id,perm_read,perm_write,perm_create,perm_unlink`
- `1` = allow, `0` = deny
- `group_id` blank = applies to all users

### __manifest__.py keys
```python
{
    'name': 'Module Name',
    'version': '16.0.1.0.0',     # Odoo version prefix required
    'depends': ['base', 'mail'],  # other modules this needs
    'data': [                     # files loaded in order
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/model_views.xml',
    ],
    'installable': True,
    'application': True,
}
```

---

## Coding conventions for this project

- One Python file per model in `models/`
- Model name pattern: `school.model_name` (e.g. `school.student`)
- Python class name: `SchoolStudent`
- File name: `student.py`
- All string labels in English
- Use `_inherit = 'mail.thread'` on main models for chatter/log notes
- Always add `_rec_name` if display name isn't `name` field

## Module technical name
`school_management`

## Security groups (defined in `security/groups.xml`)

| XML ID | Name | Implies |
|--------|------|---------|
| `group_school_student` | Student | — |
| `group_school_teacher` | Teacher | Student |
| `group_school_accountant` | Accountant | Student |
| `group_school_principal` | Principal | Teacher |
| `group_school_admin` | Administrator | Principal |

Reference in XML: `groups="school_management.group_school_admin"`
Reference in CSV: `school_management.group_school_admin`

## View types used per model

| View | When to add |
|------|-------------|
| form | always |
| tree | always |
| kanban | when records have a natural "stage" or visual grouping |
| graph | when data has numeric measures worth visualizing |
| pivot | when cross-tabulation by 2 dimensions is useful |

## Docker commands

```bash
docker-compose up -d                                           # start
docker-compose exec odoo odoo -i school_management -d odoo --stop-after-init  # install
docker-compose exec odoo odoo -u school_management -d odoo --stop-after-init  # upgrade
docker-compose logs -f odoo                                    # logs
```

## Phases (see PLAN.md for full detail)
0. Docker setup
1. Module scaffold + school info
1.5. Security — groups, roles, ir.model.access.csv
1.6. User management — res.users extension, school_role field, auto group assign, profile links
2. People — teachers (kanban), students (kanban), admissions (kanban + graph)
3. Academic structure — classes (kanban), subjects, assignments
4. Operations — timetable, attendance (graph + pivot), wizard
5. Results — exams (kanban), grades (graph + pivot), QWeb report card PDF
6. Finance — fee structure, invoices (kanban + graph + pivot), payments
