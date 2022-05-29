# -*- coding: utf-8 -*-
import logging
from odoo import fields, models, api, _

_logger = logging.getLogger(__name__)

class Department(models.Model):
    _name = 'ev.department'
    _description = 'Model for the Departments'
    _rec_name = 'name'

    name = fields.Char(
        string='Name',
        required=True,
        help='Name of Department',
    )

    description = fields.Text(
        string='Description',
        help='Description of Department',
    )

    believer_ids = fields.Many2many(
        'ev.believer',
        string='Believers',
        help='Believers of Department',
    )

    active = fields.Boolean(
        string='Active',
        default=True,
        help='Active Department',
    )