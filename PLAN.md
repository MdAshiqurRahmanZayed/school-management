# School Management — Odoo 16 Module Plan

**Module:** `school_management`
**Stack:** Odoo 16, Docker Compose, PostgreSQL
**Goal:** Learning project — one new Odoo concept per phase

---

## Build Phases

| Phase | What | Models | Views | Concept |
|-------|------|--------|-------|---------|
| 0 | Docker setup | — | — | addon path, dev mode |
| 0.5 | OCA check | — | — | `base_user_role` present in 16.0 via extra-addons ✅ |
| 1 | Module scaffold + school info | `school.info` | form (tabbed), tree | manifest, first model, security CSV, mail.thread mixin |
| 1.5 | Security groups | — | groups.xml, CSV | `res.groups`, implied groups, menu/view `groups=` ✅ |
| 2 | People | teacher, student, admission | form+tree+kanban; graph (admission) | `Many2one`, `mail.thread`, state buttons, sequences |
| 2 | People | teacher, student, admission | form+tree+kanban; graph (admission) | `Many2one`, `mail.thread`, state buttons, sequences |
| 3 | Academic structure | class, subject, class.subject | form+tree+kanban (class) | `Many2many`, `One2many`, `@api.depends` |
| 4 | Operations | timetable, attendance, wizard | graph+pivot (attendance) | `@api.constrains`, `TransientModel`, `@api.onchange` |
| 5 | Results | exam, grade, report card | kanban (exam); graph+pivot+PDF (grade) | `store=True`, QWeb PDF |
| 6 | Finance | fee.structure, fee.invoice, fee.payment | kanban+graph+pivot (invoice) | sequences, `_sql_constraints` |

---

## Security Groups

```
Administrator → Principal → Teacher → Student
                         → (parallel) Accountant → Student
```

| Group | XML ID |
|-------|--------|
| Student | `group_school_student` |
| Teacher | `group_school_teacher` |
| Accountant | `group_school_accountant` |
| Principal | `group_school_principal` |
| Administrator | `group_school_admin` |

## Access Matrix

| Model | Admin | Principal | Teacher | Accountant | Student |
|-------|-------|-----------|---------|------------|---------|
| school.info | RWCD | R | R | R | R |
| school.teacher | RWCD | RWCD | R(own) | — | — |
| school.student | RWCD | RWCD | R | R | R(own) |
| school.admission | RWCD | RWCD | R | — | — |
| school.class | RWCD | R | R | — | R |
| school.subject | RWCD | R | R | — | R |
| school.timetable | RWCD | R | R | — | R |
| school.attendance | RWCD | R | RWCD | — | R(own) |
| school.exam | RWCD | RWCD | R | — | R |
| school.grade | RWCD | R | RWCD | — | R(own) |
| school.fee.structure | RWCD | R | — | RWCD | — |
| school.fee.invoice | RWCD | R | — | RWCD | R(own) |
| school.fee.payment | RWCD | R | — | RWCD | — |

---

## Key Decisions

- **`web_responsive` (OCA)** — installed from `OCA/web` branch 16.0, lives in `extra-addons/` (gitignored)
- **`base_user_role` (OCA)** — not available in 16.0, skipped
- **`school_role` field skipped** — dual source of truth with Odoo group UI; use Settings → Users → Groups tab to assign roles
- **`school_user_management` module skipped** — adds complexity without clear learning value at this stage

## Open Questions

- Phase 4: Block room double-booking, or just teacher conflicts?
- Phase 5: Report card — single student or batch print for full class?
- Phase 6: Fee invoice — auto-create on enrollment or manual?

---

## File Structure

```
school-management/
├── docker-compose.yml
├── config/odoo.conf
├── addons/                               ← git tracked
│   ├── school_management/
│   │   ├── __init__.py / __manifest__.py
│   │   ├── models/                       ← school_info, teacher, student,
│   │   │                                    admission, school_class, subject,
│   │   │                                    class_subject, timetable, attendance,
│   │   │                                    exam, grade, fee_structure, fee_invoice,
│   │   │                                    fee_payment
│   │   ├── views/                        ← one XML per model + menu.xml
│   │   ├── wizards/                      ← attendance_wizard
│   │   ├── reports/                      ← report_card.xml (QWeb PDF)
│   │   ├── security/                     ← groups.xml, ir.model.access.csv
│   │   └── data/                         ← sequences.xml
└── extra-addons/                         ← gitignored
    └── web_responsive/                   ← OCA/web 16.0
```

---

## Docker Commands

```bash
# Start
docker-compose up -d

# Install (first time)
docker-compose exec odoo odoo -i school_management -d odoo --stop-after-init

# Upgrade after changes
docker-compose exec odoo odoo -u school_management -d odoo --stop-after-init

# Logs
docker-compose logs -f odoo

# Dev mode
# http://localhost:8069/web?debug=1
```


## Shell Access

```bash
docker-compose up -d && docker-compose exec  odoo odoo shell -d <db_name>
```
