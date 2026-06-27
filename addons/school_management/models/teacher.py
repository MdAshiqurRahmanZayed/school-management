from dateutil.relativedelta import relativedelta
from odoo import Command, _, api, fields, models
from odoo.exceptions import UserError


class SchoolTeacher(models.Model):
    _name = "school.teacher"
    _description = "Teacher"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "name"
    _order = "name"

    _sql_constraints = [
        ("email_unique", "UNIQUE(email)", "Email must be unique across teachers."),
    ]

    name = fields.Char(string="Full Name", required=True, tracking=True)
    employee_id = fields.Char(
        string="Employee ID",
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
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    address = fields.Text(string="Address")
    qualification = fields.Char(string="Qualification")
    specialization = fields.Char(string="Specialization")
    experience_years = fields.Integer(string="Years of Experience")
    join_date = fields.Date(
        string="Join Date",
        default=fields.Date.today,
        tracking=True,
    )
    state = fields.Selection(
        selection=[
            ("active", "Active"),
            ("on_leave", "On Leave"),
            ("resigned", "Resigned"),
            ("terminated", "Terminated"),
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

    def action_set_active(self):
        self.state = "active"

    def action_set_on_leave(self):
        self.state = "on_leave"

    def action_resign(self):
        self.state = "resigned"

    def action_terminate(self):
        self.state = "terminated"

    def action_create_user(self):
        self.ensure_one()
        if not self.email:
            raise UserError(_("Teacher must have an email to create a user."))
        if self.user_id:
            raise UserError(_("User already linked to this teacher."))
        teacher_group = self.env.ref("school_management.group_school_teacher")
        internal_group = self.env.ref("base.group_user")
        user = (
            self.env["res.users"]
            .sudo()
            .create(
                {
                    "name": self.name,
                    "login": self.email,
                    "email": self.email,
                }
            )
        )
        user.sudo().write(
            {
                "groups_id": [Command.set([internal_group.id, teacher_group.id])],
            }
        )
        role = self.env.ref("school_user_management.role_school_teacher", raise_if_not_found=False)
        if role:
            user.sudo().write({"role_line_ids": [(0, 0, {"role_id": role.id})]})
        self.user_id = user

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("employee_id", _("New")) == _("New"):
                vals["employee_id"] = self.env["ir.sequence"].next_by_code("school.teacher") or _("New")
        return super().create(vals_list)
