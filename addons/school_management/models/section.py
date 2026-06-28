from odoo import fields, models


class SchoolSection(models.Model):
    _name = "school.section"
    _description = "Class Section"
    _rec_name = "name"
    _order = "name"

    name = fields.Char(string="Name", required=True)
    description = fields.Char(string="Description")

    _sql_constraints = [
        ("name_unique", "UNIQUE(name)", "Section name must be unique."),
    ]
