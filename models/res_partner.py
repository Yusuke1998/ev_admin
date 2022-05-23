# -*- coding: utf-8 -*-
from odoo import models, fields, _

class Partner(models.Model):
    _inherit = ['res.partner']

    type = fields.Selection(
        selection_add = [('believer', 'believer address')]
    )
    
    believer = fields.Boolean(
        string='believer',
        required=False,
        help="Check this box if this contact is an believer."
    )