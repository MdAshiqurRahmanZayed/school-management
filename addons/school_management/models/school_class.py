from odoo import api, fields, models


class SchoolClass(models.Model):
    _name = "school.class"
    _description = "Class"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "full_name"
    _order = "academic_year_id desc, name, section_id"

    name = fields.Char(string="Grade / Class Name", required=True, tracking=True)
    section_id = fields.Many2one(
        comodel_name="school.section",
        string="Section",
        required=True,
        tracking=True,
        ondelete="restrict",
    )
    academic_year_id = fields.Many2one(
        comodel_name="school.academic.year",
        string="Academic Year",
        required=True,
        tracking=True,
        ondelete="restrict",
        default=lambda self: self._default_academic_year(),
    )
    classroom_id = fields.Many2one(
        comodel_name="school.classroom",
        string="Classroom",
        tracking=True,
        ondelete="set null",
    )
    full_name = fields.Char(
        string="Class",
        compute="_compute_full_name",
        store=True,
    )
    class_teacher_id = fields.Many2one(
        comodel_name="school.teacher",
        string="Homeroom Teacher",
        tracking=True,
        ondelete="set null",
    )
    student_ids = fields.Many2many(
        comodel_name="school.student",
        relation="school_class_student_rel",
        column1="class_id",
        column2="student_id",
        string="Students",
    )
    course_ids = fields.Many2many(
        comodel_name="school.course",
        relation="school_class_course_rel",
        column1="class_id",
        column2="course_id",
        string="Courses",
    )
    capacity = fields.Integer(string="Capacity", default=40)
    student_count = fields.Integer(
        string="Students Enrolled",
        compute="_compute_student_count",
        store=True,
    )
    state = fields.Selection(
        selection=[
            ("active", "Active"),
            ("completed", "Completed"),
            ("archived", "Archived"),
        ],
        string="Status",
        default="active",
        required=True,
        tracking=True,
        group_expand="_expand_states",
    )

    _sql_constraints = [
        (
            "class_unique",
            "UNIQUE(name, section_id, academic_year_id)",
            "A class with this name, section, and academic year already exists.",
        ),
    ]

    @api.model
    def _default_academic_year(self):
        return self.env["school.academic.year"].search([("state", "=", "active")], limit=1)

    @api.model
    def _expand_states(self, states, domain, order):
        return [key for key, _val in self._fields["state"].selection]

    @api.depends("name", "section_id", "academic_year_id")
    def _compute_full_name(self):
        for rec in self:
            parts = [rec.name or ""]
            if rec.section_id:
                parts.append(f"- {rec.section_id.name}")
            if rec.academic_year_id:
                parts.append(f"({rec.academic_year_id.name})")
            rec.full_name = " ".join(filter(None, parts))

    @api.depends("student_ids")
    def _compute_student_count(self):
        for rec in self:
            rec.student_count = len(rec.student_ids)

    def action_set_active(self):
        self.state = "active"

    def action_set_completed(self):
        self.state = "completed"

    def action_set_archived(self):
        self.state = "archived"
