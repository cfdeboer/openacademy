# -*- coding: utf-8 -*-
from openerp import fields, models

class Partner(models.Model):
    _inherit = 'res.partner'
    #_inherits = {'res.partner': 'partner_id'}
    # Add a new column to the res.partner model, by default partners are not
    # instructors
    instructor = fields.Boolean("Instructor", default=True)

    session_ids = fields.Many2many('openacademy.session',
            string="Attended Sessions", readonly=False)
