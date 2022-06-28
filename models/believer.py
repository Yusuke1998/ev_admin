# -*- coding: utf-8 -*-
import logging
from odoo import fields, models, api, _

_logger = logging.getLogger(__name__)

class Believer(models.Model):
    _name = 'ev.believer'
    _description = 'Model for the Believers'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _inherits = {'res.partner': 'partner_id'}
    _rec_name = 'name'

    from_web = fields.Boolean(
        string='From Web',
        default=False
    )

    from_mobile = fields.Boolean(
        string='From Mobile',
        default=False
    )

    partner_id = fields.Many2one(
        'res.partner',
        string='Person',
        help='Partner of Believer',
    )

    profile = fields.Boolean(
        string='Profile',
        default=False,
        help='profile Record',
    )

    identity = fields.Char(
        string="Identity"
    )

    state_id = fields.Many2one(
        'res.country.state',
        string='State'
    )

    municipality_id = fields.Many2one(
        'res.country.state.municipality',
        string='Municipality',
    )

    parish_id = fields.Many2one(
        'res.country.state.municipality.parish',
        string='Parish'
    )

    sector = fields.Char(
        string='Locality Sector',
        help='Sector of Residence'
    )

    street = fields.Char(
        string='Street / Avenue',
        help='Street of Residence'
    )

    building = fields.Char(
        string='building / premises',
        help='Building o Local of Residence'
    )

    house = fields.Char(
        string='House Number',
        help='House Number of Residence',
    )

    localphone_number = fields.Char(
        string='Local Telephone',
        help='Local Telephone Number',
        size=13
    )

    cellphone_number = fields.Char(
        string='Cell Telephone',
        help='Cell Telephone Number',
        size=13
    )

    department_ids = fields.Many2many(
        'ev.department',
        string='Departments',
        help='Departments of Believer',
    )

    active = fields.Boolean(
        string='Active',
        default=True,
        help='Active Believer',
    )

    def send_credentials(self, email, password):
        template = self.env['mail.template'].search([('model', '=', 'ev.believer')], limit=1)
        if template:
            try:
                template.with_context(
                    email=email, password=password
                ).send_mail(
                    self.id, force_send=True,
                    email_values={'email_to': email}
                )
                return True
            except Exception as e:
                _logger.error(e)
                return False
        else:
            _logger.error('Template not found')
            return False

    def unlink(self):
        for r in self:
            if r.partner_id:
                user = self.env['res.users'].search([('partner_id', '=', r.partner_id.id)])
                if user:
                    user.unlink()
                # r.partner_id.unlink()
        return super(Believer, self).unlink()