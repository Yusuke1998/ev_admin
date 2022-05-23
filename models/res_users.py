# -*- coding: utf-8 -*-
from odoo import api, models, fields, _

class Users(models.Model):
    _inherit = 'res.users'

    believer_id = fields.Many2one(
        'ev.believer',
        string='Believer',
        help='Believer of User',
    )