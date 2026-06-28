from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SchoolAcademicYear(models.Model):
    _name = "school.academic.year"
    _description = "Academic Year"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "name"
    _order = "start_date desc"

    name = fields.Char(string="Name", required=True, tracking=True)
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    state = fields.Selection(
        selection=[("draft", "Draft"), ("active", "Active"), ("closed", "Closed")],
        string="Status",
        default="draft",
        required=True,
        tracking=True,
    )
    is_current = fields.Boolean(
        string="Current Year",
        compute="_compute_is_current",
        store=True,
    )
    class_count = fields.Integer(
        string="Classes",
        compute="_compute_class_count",
    )

    @api.depends("state")
    def _compute_is_current(self):
        for rec in self:
            rec.is_current = rec.state == "active"

    def _compute_class_count(self):
        for rec in self:
            rec.class_count = self.env["school.class"].search_count([("academic_year_id", "=", rec.id)])

    @api.constrains("state")
    def _check_single_active_year(self):
        for rec in self:
            if rec.state == "active":
                existing = self.search([("state", "=", "active"), ("id", "!=", rec.id)])
                if existing:
                    raise ValidationError(
                        "Only one academic year can be active at a time. " "Deactivate '%s' first." % existing[0].name
                    )

    @api.constrains("start_date", "end_date")
    def _check_dates(self):
        for rec in self:
            if rec.start_date and rec.end_date and rec.end_date <= rec.start_date:
                raise ValidationError("End date must be after start date.")

    def action_set_active(self):
        self.state = "active"

    def action_set_closed(self):
        self.state = "closed"

    def action_set_draft(self):
        self.state = "draft"
