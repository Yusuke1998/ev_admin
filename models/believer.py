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

    def getBelievers(self):
        believers = self.search([])
        
        if len(believers) > 0:
            return {
                'status': 'success',
                'message': 'Successfully retrieved',
                'records': [{
                        'id': believer.id,
                        'name': believer.name,
                        'identity': believer.identity,
                        'state': {
                            'id': believer.state_id.id,
                            'name': believer.state_id.name
                        },
                        'municipality': {
                            'id': believer.municipality_id.id,
                            'name': believer.municipality_id.name
                        },
                        'parish': {
                            'id': believer.parish_id.id,
                            'name': believer.parish_id.name
                        },
                        'sector': believer.sector,
                        'street': believer.street,
                        'building': believer.building,
                        'house': believer.house,
                        'localphone_number': believer.localphone_number,
                        'localphone_number': believer.cellphone_number,
                        'department_ids': [{
                            'id': department.id,
                            'name': department.name
                        } for department in believer.department_ids],
                        'profile': believer.profile
                } for believer in believers ]
            }
        else:
            return {
                'status': 'error',
                'message': 'No records found',
                'records': []
            }

    def send_credentials(self, email, password):
        self.env['mail.mail'].create({
            'subject': 'Datos de acceso',
            'email_from': 'jhonny@afrus.app',
            'email_to': email,
            'body_html': '<p>Su usuario es: ' + email + '</p><p>Su contraseña es: ' + password + '</p>',
            'state': 'outgoing'
        }).send()

