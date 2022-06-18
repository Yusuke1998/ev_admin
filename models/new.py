# -*- coding: utf-8 -*-
from email.policy import default
import logging
from odoo import fields, models, api, _
from odoo.exceptions import UserError

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

    content = fields.Html('Content', sanitize=False)

    date = fields.Date(
        string='Date',
        help='Date of News',
        required=True,
        default=fields.Date.today(),
    )

    expiry_date = fields.Date(
        string='Expiry Date',
        help='Expiry Date of News',
    )

    image = fields.Binary(
        string='Image',
        help='Image of News',
    )

    image_url = fields.Char(
        string='Image URL',
        help='Image URL of News',
    )

    category_id = fields.Many2one(
        'ev.new.category',
        string='Category',
        help='Category of News',
    )

    state = fields.Selection(
        string='Status',
        selection=[
            ('draft', 'Draft'),
            ('published', 'Published'),
            ('expired', 'Expired'),
            ('deleted', 'Deleted'),
        ],
        default='draft',
        help='Status of News',
    )

    active = fields.Boolean(
        string='Active',
        default=True,
        help='Active News',
    )

    @api.model
    def create(self, vals):
        if not vals.get('category_id', False):
            vals['category_id'] = self.env.ref('ev_new.new_category1').id
        return super().create(vals)

    def verify_expiry_cron(self):
        records = self.env['ev.new'].search([
            ('expiry_date', '!=', False),
            ('expiry_date', '<=', fields.Date.today()),
            ('state', '=', 'published'),
        ])
        for record in records:
            record.state = 'expired'

    def publish(self):
        if self.state == 'draft':
            self.state = 'published'
        else:
            raise UserError(_('News must be in draft state to publish'))

    def to_draft(self):
        if self.state != 'draft':
            self.state = 'draft'
            self.active = True
        else:
            raise UserError(_('News must be in published state to draft'))

    def delete(self):
        if self.state == 'draft':
            self.state = 'deleted'
            self.active = False
        else:
            raise UserError(_('News must be in draft state to delete'))

class NewsCategory(models.Model):
    _name = 'ev.new.category'
    _description = 'Model for the News Category'
    _rec_name = 'name'

    name = fields.Char(
        string='Name',
        required=True,
        help='Name of News Category',
    )

    description = fields.Text(
        string='Description',
        help='Description of News Category',
    )

    active = fields.Boolean(
        string='Active',
        default=True,
        help='Active News Category',
    )

    @api.model
    def create(self, vals):
        if vals.get('name', False):
            vals['name'] = vals['name'].upper()
        return super().create(vals)

    def deactivate(self):
        if self.active:
            self.active = False
        else:
            raise UserError(_('News Category must be active to delete'))

    def to_active(self):
        if not self.active:
            self.active = True
        else:
            raise UserError(_('News Category must be inactive to undelete'))