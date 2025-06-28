from odoo import models, fields,api
from datetime import date
from odoo.exceptions import ValidationError
import re
from odoo.exceptions import AccessError


class HMSPatientLog(models.Model):
    _name = "patient.log"
    _description = "Patient Log History"


    created_by = fields.Many2one('res.users', string="Created By",default=lambda self: self.env.user)
    date = fields.Datetime(string="Date", default=fields.Datetime.now)
    description = fields.Text(string="Description")
    patient_id = fields.Many2one('patient', string="Patient")



class HMSPatient(models.Model):
    _name = "patient"
    _description = "Patient"


    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    birth_date = fields.Date(string="Birth Date")
    cr_ratio = fields.Float(string="CR Ratio")
    history = fields.Html(string="Medical History")
    blood_type = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O')
    ], string="Blood Type")
    pcr = fields.Boolean(string="PCR Test")
    image = fields.Image(string="Patient Image")
    address = fields.Text(string="Address")
    age = fields.Integer(string="Age",compute='_compute_age',store=True)
    department_id = fields.Many2one('hms_departments', string="Department")
    doctor_ids = fields.Many2many('hms_doctors', string="Doctors",)
    department_capacity = fields.Integer(string="Department Capacity", related="department_id.capacity", readonly=True)
    # department_is_opened = fields.Boolean(string="Department status",related="department_id.is_opened")
    log_ids = fields.One2many('patient.log', 'patient_id', string="Log History")
    state= fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ])
    email = fields.Char(string='Email',tracking=True,help="Patient's unique email address")
    related_partner_id = fields.One2many( 'res.partner','related_patient_id',string='Related Customer')
    created_by = fields.Many2one('res.users', string="Created By", default=lambda self: self.env.user, readonly=True)

    @api.onchange('pcr')
    def set_cr_ratio(self):
        if self.pcr and not self.cr_ratio:
            return {
                'warning':{
                    'title':'CR Ratio Required',
                    'message':'If PCR is checked, CR Ratio cannot be Null'
                }
            }
    def confirm_action(self):
        print("in function Approve")

    def add_log(self, description):
        self.env['patient.log'].create({
            'patient_id': self.id,
            'description': description
        })
        return True

    def write(self, vals):
        if 'state' in vals:
            state_mapping = dict(self._fields['state'].selection)
            description = f"State changed to {state_mapping.get(vals['state'], vals['state'])}"
            self.add_log(description)
        return super(HMSPatient, self).write(vals)

##pcr is Tru if age < 30
    @api.onchange('age')
    def age_check_pcr(self):
        if self.age and self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': "PCR Auto-Checked",
                    'message': "PCR has been automatically checked because patient age is under 30"
                }
            }
        elif self.age:  # Only uncheck if age has a value
            self.pcr = False

    ##Check email
    @api.constrains('email')
    def _check_valid_email(self):
        for record in self:
            if record.email:
                if not re.match(r'^[^@]+@[^@]+\.[^@]+$', record.email):
                    raise ValidationError("Please enter a valid email address (e.g., name@example.com)")
    _sql_constraints = [
        ('email_unique', 'UNIQUE(email)', 'Email address must be unique per patient!')]

## calculate the age

    @api.depends('birth_date')
    def _compute_age(self):
        today = date.today()
        for patient in self:
            if patient.birth_date:
                birth_date = fields.Date.from_string(patient.birth_date)
                age = today.year - birth_date.year
                patient.age = age
            else:
                patient.age = 0