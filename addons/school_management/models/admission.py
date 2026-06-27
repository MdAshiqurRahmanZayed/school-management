from dateutil.relativedelta import relativedelta
from odoo import Command, _, api, fields, models
from odoo.exceptions import UserError


class SchoolAdmission(models.Model):
    _name = "school.admission"
    _description = "Admission Application"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "application_no"
    _order = "application_date desc"

    _sql_constraints = [
        ("email_unique", "UNIQUE(email)", "Email must be unique across admission applications."),
    ]

    application_no = fields.Char(
        string="Application No.",
        readonly=True,
        copy=False,
        default=lambda self: _("New"),
    )
    student_name = fields.Char(string="Applicant Name", required=True, tracking=True)
    photo = fields.Image(string="Photo", max_width=1024, max_height=1024)
    gender = fields.Selection(
        selection=[("male", "Male"), ("female", "Female"), ("other", "Other")],
        string="Gender",
    )
    date_of_birth = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age", compute="_compute_age")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    address = fields.Text(string="Address")
    guardian_name = fields.Char(string="Guardian Name")
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
    applied_class = fields.Char(string="Applying for Class")
    application_date = fields.Date(
        string="Application Date",
        default=fields.Date.today,
        tracking=True,
    )
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("submitted", "Submitted"),
            ("under_review", "Under Review"),
            ("admitted", "Admitted"),
            ("rejected", "Rejected"),
        ],
        string="Status",
        default="draft",
        tracking=True,
        group_expand="_expand_states",
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Created User",
        readonly=True,
        tracking=True,
        ondelete="set null",
    )
    student_id = fields.Many2one(
        comodel_name="school.student",
        string="Enrolled Student",
        readonly=True,
        tracking=True,
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

    def action_submit(self):
        self.state = "submitted"

    def action_review(self):
        self.state = "under_review"

    def action_admit(self):
        self.state = "admitted"

    def action_reject(self):
        self.state = "rejected"

    def action_reset_draft(self):
        self.state = "draft"

    def action_create_user(self):
        self.ensure_one()
        if not self.email:
            raise UserError(_("Applicant must have an email to create a user."))
        if self.user_id:
            raise UserError(_("User already created for this application."))
        student_group = self.env.ref("school_management.group_school_student")
        internal_group = self.env.ref("base.group_user")
        user = (
            self.env["res.users"]
            .sudo()
            .create(
                {
                    "name": self.student_name,
                    "login": self.email,
                    "email": self.email,
                }
            )
        )
        user.sudo().write(
            {
                "groups_id": [Command.set([internal_group.id, student_group.id])],
            }
        )
        self.user_id = user

    def action_create_student(self):
        self.ensure_one()
        if self.state != "admitted":
            raise UserError(_("Only admitted applicants can be enrolled as students."))
        if not self.user_id:
            raise UserError(_("Create a user first before enrolling as student."))
        if self.student_id:
            raise UserError(_("Student record already created for this application."))
        existing = self.env["school.student"].search([("email", "=", self.email)], limit=1)
        if existing:
            raise UserError(_("A student with email '%s' already exists: %s") % (self.email, existing.name))
        student = self.env["school.student"].create(
            {
                "name": self.student_name,
                "photo": self.photo,
                "gender": self.gender,
                "date_of_birth": self.date_of_birth,
                "phone": self.phone,
                "email": self.email,
                "address": self.address,
                "guardian_name": self.guardian_name,
                "guardian_phone": self.guardian_phone,
                "guardian_relation": self.guardian_relation,
                "user_id": self.user_id.id,
            }
        )
        self.student_id = student

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("application_no", _("New")) == _("New"):
                vals["application_no"] = self.env["ir.sequence"].next_by_code("school.admission") or _("New")
        return super().create(vals_list)
