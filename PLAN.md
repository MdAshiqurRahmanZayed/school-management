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
| 2 | People | `school.teacher`, `school.student`, `school.admission` | form+tree+kanban; graph (admission) | `Many2one`, `mail.thread`, state buttons, sequences ✅ |
| 3 | Academic structure | `school.academic.year`, `school.section`, `school.classroom`, `school.class`, `school.course`, `school.assignment`, `school.assignment.submission` (assignment submission) | kanban (class, assignment), form+tree all | `Many2many`, `One2many`, `@api.depends`, `ir.rule` record rules, computed fields |
| 4 | Operations | `school.timetable`, `school.attendance` + wizard | graph+pivot (attendance) | `@api.constrains`, `TransientModel`, `@api.onchange` |
| 5 | Results | `school.exam`, `school.grade`, report card | kanban (exam); graph+pivot+PDF (grade) | `store=True`, QWeb PDF |
| 6 | Finance | `school.fee.structure`, `school.fee.invoice`, `school.fee.payment` | kanban+graph+pivot (invoice) | sequences, `_sql_constraints` |

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
| school.teacher | RWCD | RWCD | R | — | — |
| school.student | RWCD | RWCD | R | R | R(own) |
| school.admission | RWCD | RWCD | R | — | — |
| school.academic.year | RWCD | RWC | R | R | R |
| school.section | RWCD | RWCD | R | — | R |
| school.classroom | RWCD | RWCD | R | — | R |
| school.class | RWCD | RWCD | RWCD(own via ir.rule) | R | R(own via ir.rule) |
| school.course | RWCD | RWCD | RWCD(own via ir.rule) | R | R(own via ir.rule) |
| school.assignment | RWCD | RWCD | RWCD(own via ir.rule) | — | R(own+published via ir.rule) |
| school.assignment.submission | RWCD | RWCD | RWCD(own via ir.rule) | — | RWC(own via ir.rule) |
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
- **`base_user_role` (OCA)** — present in `extra-addons/`, used by `school_user_management` module ✅
- **`school_user_management` module** — separate addon for user/role management, depends on `base_user_role`
- **`school.section` as model** — not free text; managed dropdown so sections are consistent across years
- **`school.academic.year` as model** — scopes all classes; constraint: only one active year at a time
- **`school.classroom` as model** — physical room tracked separately from class group; allows capacity/type management
- **`school.course` (not `subject`)** — clearer naming for what is taught; code auto-computed from name, user-editable
- **`ir.rule` record rules** — students see only own class data; bridge via `school.student.user_id`
- **Student "My Class" menu** — uses `group_school_student`; teachers also see it (Option A — simple) since teacher implies student; record rules are the real security wall
- **`school.assignment.submission` = Assignment Submission** — not exam results; tracks student answer (Html), file attachments, and teacher grading in one record; state: `draft → submitted → graded`; exam results are `school.grade` in Phase 5

## Open Questions

- Phase 4: Block room double-booking in timetable, or just flag teacher conflicts?
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
│   │   ├── models/
│   │   │   ├── school_info.py
│   │   │   ├── teacher.py
│   │   │   ├── student.py            ← class_id added in Phase 3
│   │   │   ├── admission.py
│   │   │   ├── academic_year.py      ← Phase 3
│   │   │   ├── section.py            ← Phase 3
│   │   │   ├── classroom.py          ← Phase 3
│   │   │   ├── class.py              ← Phase 3
│   │   │   ├── course.py             ← Phase 3
│   │   │   ├── assignment.py         ← Phase 3
│   │   │   ├── result.py             ← Phase 3
│   │   │   ├── timetable.py          ← Phase 4
│   │   │   └── attendance.py         ← Phase 4
│   │   ├── views/                    ← one XML per model + menu.xml
│   │   ├── wizards/                  ← attendance_wizard (Phase 4)
│   │   ├── reports/                  ← report_card.xml QWeb PDF (Phase 5)
│   │   ├── security/
│   │   │   ├── groups.xml
│   │   │   ├── student_rules.xml     ← Phase 3 ir.rule record rules
│   │   │   └── ir.model.access.csv
│   │   └── data/
│   │       └── sequences.xml
│   └── school_user_management/       ← separate addon
└── extra-addons/                     ← gitignored
    ├── web_responsive/
    └── base_user_role/
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
docker-compose up -d && docker-compose exec odoo odoo shell -d odoo
```
