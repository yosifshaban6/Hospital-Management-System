from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Department(models.Model):
    _name = 'hms.department'
    _description = 'Department'

    name = fields.Char(required=True)
    capacity = fields.Integer()
    is_opened = fields.Boolean()
    patient_ids = fields.One2many('hms.patient', 'department_id')

    @api.constrains('is_opened')
    def _check_opened(self):
        for rec in self:
            if not rec.is_opened:
                raise ValidationError("Cannot save a department that is not opened.")