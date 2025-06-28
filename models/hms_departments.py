from odoo import models ,fields


class HMSDepartments(models.Model):
    _name = "hms_departments"

    name= fields.Char()
    capacity = fields.Integer()
    is_opened = fields.Boolean()
