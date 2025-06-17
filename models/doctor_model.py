from odoo import models, fields

class Doctor(models.Model):
    _name = 'hms.doctor'
    _description = 'Doctor'

    first_name = fields.Char(required=True)
    last_name = fields.Char()
    image = fields.Binary()
    patients_ids = fields.Many2many('hms.patient')