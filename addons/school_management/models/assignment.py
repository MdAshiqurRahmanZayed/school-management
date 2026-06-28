from odoo import _, api, fields, models


class SchoolAssignment(models.Model):
    _name = "school.assignment"
    _description = "Assignment"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "name"
    _order = "due_date desc, name"

    assignment_id = fields.Char(
        string="Assignment ID",
        readonly=True,
        copy=False,
        default=lambda self: _("New"),
    )
    name = fields.Char(string="Title", required=True, tracking=True)
    course_id = fields.Many2one(
        comodel_name="school.course",
        string="Course",
        required=True,
        tracking=True,
        ondelete="restrict",
    )
    class_id = fields.Many2one(
        comodel_name="school.class",
        string="Class",
        required=True,
        tracking=True,
        ondelete="restrict",
    )
    teacher_id = fields.Many2one(
        comodel_name="school.teacher",
        string="Assigned By",
        tracking=True,
        ondelete="set null",
    )
    academic_year_id = fields.Many2one(
        comodel_name="school.academic.year",
        string="Academic Year",
        tracking=True,
        ondelete="set null",
    )
    due_date = fields.Date(string="Due Date", tracking=True)
    max_marks = fields.Float(string="Max Marks", default=100.0)
    description = fields.Html(string="Description")
    submission_ids = fields.One2many(
        comodel_name="school.assignment.submission",
        inverse_name="assignment_id",
        string="Submissions",
    )
    submission_count = fields.Integer(
        string="Submissions",
        compute="_compute_submission_count",
    )
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("published", "Published"),
            ("closed", "Closed"),
        ],
        string="Status",
        default="draft",
        required=True,
        tracking=True,
        group_expand="_expand_states",
    )

    @api.model
    def _expand_states(self, states, domain, order):
        return [key for key, _val in self._fields["state"].selection]

    @api.depends("submission_ids")
    def _compute_submission_count(self):
        for rec in self:
            rec.submission_count = len(rec.submission_ids)

    @api.onchange("class_id")
    def _onchange_class_id(self):
        if self.class_id:
            self.academic_year_id = self.class_id.academic_year_id

    def action_publish(self):
        self.state = "published"

    def action_reset_draft(self):
        self.state = "draft"

    def action_close(self):
        self.state = "closed"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("assignment_id", _("New")) == _("New"):
                vals["assignment_id"] = self.env["ir.sequence"].next_by_code("school.assignment") or _("New")
        return super().create(vals_list)
