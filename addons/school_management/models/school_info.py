from odoo import fields, models


class SchoolInfo(models.Model):
    _name = "school.info"
    _description = "School Information"
    _rec_name = "name"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    # --- Identity ---
    name = fields.Char(string="School Name", required=True, tracking=True)
    code = fields.Char(string="Short Code", help="Abbreviation used in IDs, e.g. NHS")
    tagline = fields.Char(string="Tagline / Motto")
    school_type = fields.Selection(
        [
            ("primary", "Primary School"),
            ("secondary", "Secondary School"),
            ("higher_secondary", "Higher Secondary"),
            ("college", "College"),
            ("university", "University"),
            ("coaching", "Coaching Center"),
        ],
        string="School Type",
        default="secondary",
        tracking=True,
    )
    affiliation_board = fields.Char(string="Affiliation Board", help="e.g. National Curriculum, Cambridge, IB")
    registration_no = fields.Char(string="Registration No.")
    established_year = fields.Integer(string="Established Year")

    # --- Contact ---
    phone = fields.Char(string="Phone")
    mobile = fields.Char(string="Mobile")
    email = fields.Char(string="Email")
    website = fields.Char(string="Website")

    # --- Address ---
    street = fields.Char(string="Street")
    street2 = fields.Char(string="Street 2")
    city = fields.Char(string="City")
    state_id = fields.Many2one("res.country.state", string="State")
    country_id = fields.Many2one("res.country", string="Country")
    zip = fields.Char(string="ZIP")

    # --- Branding ---
    logo = fields.Image(string="Logo", max_width=256, max_height=256)

    # --- Academic Calendar ---
    academic_year = fields.Char(string="Current Academic Year", help="e.g. 2024-25")
    session_start = fields.Date(string="Session Start")
    session_end = fields.Date(string="Session End")

    # --- Leadership ---
    principal_id = fields.Many2one("res.users", string="Principal")
    vice_principal_id = fields.Many2one("res.users", string="Vice Principal")

    # --- Capacity ---
    total_capacity = fields.Integer(string="Total Student Capacity")

    # --- Meta ---
    active = fields.Boolean(string="Active", default=True)
    notes = fields.Html(string="Notes")
