# -*- coding: utf-8 -*-
import logging
from odoo import fields, models, api, _

_logger = logging.getLogger(__name__)

class News(models.Model):
    _name = 'ev.new'
    _description = 'Model for the News'
    _rec_name = 'title'

    title = fields.Char(
        string='Title',
        required=True,
        help='Title of News',
    )

    description = fields.Text(
        string='Description',
        help='Description of News',
    )

    active = fields.Boolean(
        string='Active',
        default=True,
        help='Active News',
    )