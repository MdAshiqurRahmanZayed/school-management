from odoo import api, fields, models


class SchoolClassroom(models.Model):
    _name = "school.classroom"
    _description = "Classroom"
    _rec_name = "name"
    _order = "name"

    name = fields.Char(string="Room Name", required=True)
    room_type = fields.Selection(
        selection=[
            ("classroom", "Classroom"),
            ("lab", "Laboratory"),
            ("library", "Library"),
            ("auditorium", "Auditorium"),
            ("sports_hall", "Sports Hall"),
        ],
        string="Room Type",
        required=True,
        default="classroom",
    )
    building = fields.Char(string="Building")
    floor = fields.Integer(string="Floor")
    capacity = fields.Integer(string="Capacity")
    class_ids = fields.One2many(
        comodel_name="school.class",
        inverse_name="classroom_id",
        string="Classes",
    )
    class_count = fields.Integer(
        string="Classes",
        compute="_compute_class_count",
    )
    notes = fields.Text(string="Notes")

    @api.depends("class_ids")
    def _compute_class_count(self):
        for rec in self:
            rec.class_count = len(rec.class_ids)
