from odoo import api, fields, models


class SchoolCourse(models.Model):
    _name = "school.course"
    _description = "Course"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "name"
    _order = "name"

    name = fields.Char(string="Course Name", required=True, tracking=True)
    code = fields.Char(
        string="Code",
        compute="_compute_code",
        store=True,
        readonly=False,
        tracking=True,
    )
    description = fields.Text(string="Description")
    teacher_ids = fields.Many2many(
        comodel_name="school.teacher",
        relation="school_course_teacher_rel",
        column1="course_id",
        column2="teacher_id",
        string="Teachers",
    )
    class_ids = fields.Many2many(
        comodel_name="school.class",
        relation="school_class_course_rel",
        column1="course_id",
        column2="class_id",
        string="Classes",
    )
    assignment_ids = fields.One2many(
        comodel_name="school.assignment",
        inverse_name="course_id",
        string="Assignments",
    )
    assignment_count = fields.Integer(
        string="Assignments",
        compute="_compute_assignment_count",
    )
    teacher_count = fields.Integer(
        string="Teachers",
        compute="_compute_teacher_count",
    )

    @api.depends("name")
    def _compute_code(self):
        for rec in self:
            if rec.name and not rec.code:
                rec.code = rec.name[:4].upper()

    @api.depends("assignment_ids")
    def _compute_assignment_count(self):
        for rec in self:
            rec.assignment_count = len(rec.assignment_ids)

    @api.depends("teacher_ids")
    def _compute_teacher_count(self):
        for rec in self:
            rec.teacher_count = len(rec.teacher_ids)
