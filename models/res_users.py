# -*- coding: utf-8 -*-
from odoo import api, models, fields, _

class Users(models.Model):
    _inherit = 'res.users'

    believer_id = fields.Many2one(
        'ev.believer',
        string='Believer',
        help='Believer of User',
    )

    @api.model
    def create(self, vals):
        if vals.get('believer_id'):
            vals.update({
                'believer_id': vals.get('believer_id')
            })
        return super(Users, self).create(vals)