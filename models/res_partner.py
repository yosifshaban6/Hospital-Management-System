from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one(
        'patient',
        string='Related Patient'
    )