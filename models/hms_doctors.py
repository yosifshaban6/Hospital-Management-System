from odoo import models ,fields

class HMSDoctors(models.Model):
    _name = "hms_doctors"

    first_name = fields.Char()
    last_name = fields.Char()
    image = fields.Binary()
    department_id = fields.Many2one('hms_departments')