from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class SchoolAssignmentSubmission(models.Model):
    _name = "school.assignment.submission"
    _description = "Assignment Submission"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "name"
    _order = "assignment_id, student_id"

    name = fields.Char(string="Name", compute="_compute_name", store=True)
    is_student_user = fields.Boolean(
        compute="_compute_is_student_user",
        help="True if current user is a student (not teacher/admin).",
    )

    assignment_id = fields.Many2one(
        comodel_name="school.assignment",
        string="Assignment",
        required=True,
        ondelete="cascade",
    )
    student_id = fields.Many2one(
        comodel_name="school.student",
        string="Student",
        required=True,
        ondelete="cascade",
        default=lambda self: self._default_student_id(),
    )
    class_id = fields.Many2one(
        comodel_name="school.class",
        string="Class",
        related="assignment_id.class_id",
        store=True,
    )
    course_id = fields.Many2one(
        comodel_name="school.course",
        string="Course",
        related="assignment_id.course_id",
        store=True,
    )
    academic_year_id = fields.Many2one(
        comodel_name="school.academic.year",
        string="Academic Year",
        related="assignment_id.academic_year_id",
        store=True,
    )

    # Submission
    answer_text = fields.Html(string="Answer")
    attachment_ids = fields.Many2many(
        comodel_name="ir.attachment",
        relation="school_assignment_submission_attachment_rel",
        column1="submission_id",
        column2="attachment_id",
        string="Attachments",
    )
    submitted_on = fields.Datetime(string="Submitted On", readonly=True, tracking=True)

    # Grading
    max_marks = fields.Float(
        string="Max Marks",
        related="assignment_id.max_marks",
        store=True,
    )
    marks_obtained = fields.Float(string="Marks Obtained", tracking=True)
    percentage = fields.Float(
        string="Percentage (%)",
        compute="_compute_percentage_grade",
        store=True,
        digits=(6, 2),
    )
    grade = fields.Selection(
        selection=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D"), ("F", "F")],
        string="Grade",
        compute="_compute_percentage_grade",
        store=True,
    )
    remarks = fields.Text(string="Remarks")
    graded_by = fields.Many2one(
        comodel_name="school.teacher",
        string="Graded By",
        ondelete="set null",
    )

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("submitted", "Submitted"),
            ("graded", "Graded"),
        ],
        string="Status",
        default="draft",
        required=True,
        tracking=True,
    )

    _sql_constraints = [
        (
            "submission_unique",
            "UNIQUE(assignment_id, student_id)",
            "A submission already exists for this student and assignment.",
        ),
    ]

    @api.model
    def _default_student_id(self):
        student = self.env["school.student"].search([("user_id", "=", self.env.uid)], limit=1)
        return student.id

    @api.depends_context("uid")
    def _compute_is_student_user(self):
        is_teacher = self.env.user.has_group("school_management.group_school_teacher")
        for rec in self:
            rec.is_student_user = not is_teacher

    @api.depends("assignment_id", "student_id")
    def _compute_name(self):
        for rec in self:
            rec.name = f"{rec.student_id.name or ''} — {rec.assignment_id.name or ''}"

    @api.depends("marks_obtained", "max_marks")
    def _compute_percentage_grade(self):
        for rec in self:
            if rec.max_marks:
                rec.percentage = (rec.marks_obtained / rec.max_marks) * 100
            else:
                rec.percentage = 0.0
            pct = rec.percentage
            if pct >= 90:
                rec.grade = "A"
            elif pct >= 80:
                rec.grade = "B"
            elif pct >= 70:
                rec.grade = "C"
            elif pct >= 60:
                rec.grade = "D"
            else:
                rec.grade = "F"

    @api.constrains("marks_obtained", "max_marks")
    def _check_marks(self):
        for rec in self:
            if rec.marks_obtained < 0:
                raise ValidationError("Marks obtained cannot be negative.")
            if rec.max_marks and rec.marks_obtained > rec.max_marks:
                raise ValidationError(
                    f"Marks obtained ({rec.marks_obtained}) cannot exceed " f"max marks ({rec.max_marks})."
                )

    def action_submit(self):
        for rec in self:
            if rec.state != "draft":
                raise UserError("Only draft submissions can be submitted.")
            rec.write({"state": "submitted", "submitted_on": fields.Datetime.now()})

    def action_mark_graded(self):
        for rec in self:
            if rec.state != "submitted":
                raise UserError("Only submitted assignments can be graded.")
            teacher = self.env["school.teacher"].search([("user_id", "=", self.env.uid)], limit=1)
            vals = {"state": "graded"}
            if teacher and not rec.graded_by:
                vals["graded_by"] = teacher.id
            rec.write(vals)

    def action_reset_draft(self):
        for rec in self:
            rec.write({"state": "draft", "submitted_on": False})
