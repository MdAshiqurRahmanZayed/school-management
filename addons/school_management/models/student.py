from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models


class SchoolStudent(models.Model):
    _name = "school.student"
    _description = "Student"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "name"
    _order = "name"

    _sql_constraints = [
        ("email_unique", "UNIQUE(email)", "Email must be unique across students."),
    ]

    name = fields.Char(string="Full Name", required=True, tracking=True)
    student_id = fields.Char(
        string="Student ID",
        readonly=True,
        copy=False,
        default=lambda self: _("New"),
    )
    photo = fields.Image(string="Photo", max_width=1024, max_height=1024)
    gender = fields.Selection(
        selection=[("male", "Male"), ("female", "Female"), ("other", "Other")],
        string="Gender",
        tracking=True,
    )
    date_of_birth = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age", compute="_compute_age")
    blood_group = fields.Selection(
        selection=[
            ("a+", "A+"),
            ("a-", "A-"),
            ("b+", "B+"),
            ("b-", "B-"),
            ("o+", "O+"),
            ("o-", "O-"),
            ("ab+", "AB+"),
            ("ab-", "AB-"),
        ],
        string="Blood Group",
    )
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    address = fields.Text(string="Address")
    guardian_name = fields.Char(string="Guardian Name", tracking=True)
    guardian_phone = fields.Char(string="Guardian Phone")
    guardian_relation = fields.Selection(
        selection=[
            ("father", "Father"),
            ("mother", "Mother"),
            ("brother", "Brother"),
            ("sister", "Sister"),
            ("other", "Other"),
        ],
        string="Guardian Relation",
    )
    enrollment_date = fields.Date(
        string="Enrollment Date",
        default=fields.Date.today,
        tracking=True,
    )
    state = fields.Selection(
        selection=[
            ("active", "Active"),
            ("graduated", "Graduated"),
            ("withdrawn", "Withdrawn"),
            ("transferred", "Transferred"),
        ],
        string="Status",
        default="active",
        tracking=True,
        group_expand="_expand_states",
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Related User",
        ondelete="set null",
    )
    notes = fields.Text(string="Notes")

    @api.model
    def _expand_states(self, states, domain, order):
        return [key for key, _val in self._fields["state"].selection]

    @api.depends("date_of_birth")
    def _compute_age(self):
        today = fields.Date.today()
        for rec in self:
            if rec.date_of_birth:
                rec.age = relativedelta(today, rec.date_of_birth).years
            else:
                rec.age = 0

    def action_graduate(self):
        self.state = "graduated"

    def action_withdraw(self):
        self.state = "withdrawn"

    def action_transfer(self):
        self.state = "transferred"

    def action_reactivate(self):
        self.state = "active"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("student_id", _("New")) == _("New"):
                vals["student_id"] = self.env["ir.sequence"].next_by_code("school.student") or _("New")
        return super().create(vals_list)
