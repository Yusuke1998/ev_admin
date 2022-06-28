# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from datetime import datetime as dt
import json
import logging

_logger = logging.getLogger(__name__)

class MobileController(http.Controller):

    @http.route('/register/believer', type='json', auth="user", methods=['POST'])
    def RegisterBeliever(self, **post):
        model_believer = request.env['ev.believer']
        model_user = request.env['res.users']
        believer = model_believer.create({
            'profile': False,
            'from_mobile': True,
            'name': post.get('name'),
        })
        email, password = post.get('email'), post.get('password')
        user = model_user.create({
            'login': email,
            'password': password,
            'partner_id': believer.partner_id.id,
            'believer_id': believer.id
        })
        user.write({
            'groups_id': [(4, request.env.ref('ev_admin.group_rol_believer').id)]
        })

        if believer:
            if believer.send_credentials(email, password):
                _logger.info('Credentials sent to %s' % email)
            else:
                _logger.error('Error sending credentials to %s' % email)

            return json.dumps({
                'status': 'success',
                'message': 'Successfully registered',
                'record': {
                    'id': believer.id
                }
            })
        else:
            return json.dumps({
                'status': 'error',
                'message': 'Error registering'
            })

    @http.route('/update/believer/<model("ev.believer"):believer>', type='json', auth="user", methods=['POST'])
    def UpdateBeliever(self, believer, **post):
        model_user = request.env['res.users']
        fields = [
            'name', 'identity', 'state_id',
            'municipality_id', 'parish_id',
            'sector', 'street', 'building',
            'house', 'localphone_number', 'cellphone_number'
        ]; values = {}
        for field in fields:
            if post.get(field):
                values[field] = post.get(field)
        if believer:
            believer.write(values)
            user = model_user.search([('believer_id', '=', believer.id)])
            if user:
                if post.get('password'):
                    user.write({ 'password': post.get('password') })
            return json.dumps({
                'status': 'success',
                'message': 'Successfully updated',
                'record': {
                    'id': believer.id
                }
            })
        else:
            return json.dumps({
                'status': 'error',
                'message': 'Error updating'
            })

    @http.route('/believers', type='json', auth="user", methods=['POST'])
    def GetBelievers(self, **post):
        model_believer = request.env['ev.believer']
        believers = model_believer.search([('active', '=', True)])

        if believers:
            return json.dumps({
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
            })
        else:
            return json.dumps({
                'status': 'error',
                'message': 'Error retrieving'
            })

    @http.route(['/believer/<model("ev.believer"):believer>', '/believer/p/<model("res.partner"):partner>'], type='json', auth="user", methods=['POST'])
    def GetBeliever(self, believer=0, partner=0, **post):
        if partner:
            believer = request.env['ev.believer'].search([('partner_id', '=', partner.id)])
        if believer:
            return json.dumps({
                'status': 'success',
                'message': 'Successfully retrieved',
                'record': {
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
                    'cellphone_number': believer.cellphone_number,
                    'department_ids': [{
                        'id': department.id,
                        'name': department.name
                    } for department in believer.department_ids],
                    'profile': believer.profile                    
                }
            })
        else:
            return json.dumps({
                'status': 'error',
                'message': 'Error retrieving'
            })

    @http.route('/departments', type='json', auth="user", methods=['POST'])
    def GetDepartments(self, **post):
        model_department = request.env['ev.department']
        departments = model_department.search([('active', '=', True)])

        if departments:
            return json.dumps({
                'status': 'success',
                'message': 'Successfully retrieved',
                'records': [
                    {
                        'id': department.id,
                        'name': department.name,
                        'believer_ids': [{
                            'id': believer.id,
                            'name': believer.name
                        } for believer in department.believer_ids],
                    } for department in departments
                ]
            })
        else:
            return json.dumps({
                'status': 'error',
                'message': 'Error retrieving'
            })
    
    @http.route('/department/<int:department_id>', type='json', auth="user", methods=['POST'])
    def GetDepartment(self, department_id, **post):
        model_department = request.env['ev.department']
        department = model_department.search([('id', '=', department_id)])

        if department:
            return json.dumps({
                'status': 'success',
                'message': 'Successfully retrieved',
                'record': {
                    'id': department.id,
                    'name': department.name,
                    'believer_ids': [{
                        'id': believer.id,
                        'name': believer.name
                    } for believer in department.believer_ids],
                }
            })
        else:
            return json.dumps({
                'status': 'error',
                'message': 'Error retrieving'
            })

    @http.route('/news', type='json', auth="user", methods=['POST'])
    def GetNews(self, **post):
        model_news = request.env['ev.new']
        news = model_news.search([
            ('state', '=', 'published'),
        ], order='date desc')

        if news:
            return json.dumps({
                'status': 'success',
                'message': 'Successfully retrieved',
                'records': [{
                    'id': new.id,
                    'title': new.title,
                    'description': new.description,
                    'content': new.content,
                    'date': new.date.strftime('%Y-%m-%d') if new.date  else False,
                    'expiry_date': new.expiry_date.strftime('%Y-%m-%d') if new.expiry_date else False,
                    'image': new.image,
                    'image_url': new.image_url,
                    'category': {
                        'id': new.category_id.id,
                        'name': new.category_id.name
                    },
                    'state': new.state
                } for new in news]
            })
        else:
            return json.dumps({
                'status': 'error',
                'message': 'Error retrieving'
            })

    @http.route('/new/<int:new_id>', type='json', auth="user", methods=['POST'])
    def GetNew(self, new_id, **post):
        model_news = request.env['ev.new']
        new = model_news.search([('id', '=', new_id)])

        if new:
            return json.dumps({
                'status': 'success',
                'message': 'Successfully retrieved',
                'record': {
                    'id': new.id,
                    'title': new.title,
                    'description': new.description,
                    'content': new.content,
                    'date': new.date.strftime('%Y-%m-%d') if new.date  else False,
                    'expiry_date': new.expiry_date.strftime('%Y-%m-%d') if new.expiry_date else False,
                    'image': new.image,
                    'image_url': new.image_url,
                    'category': {
                        'id': new.category_id.id,
                        'name': new.category_id.name
                    },
                    'state': new.state
                }
            })
        else:
            return json.dumps({
                'status': 'error',
                'message': 'Error retrieving'
            })

    @http.route('/roles/<model("res.users"):user>', type='json', auth="user", methods=['POST'])
    def GetRoles(self, user=0, **post):
        if user:
            return json.dumps({
                'status': 'success',
                'message': 'Successfully retrieved',
                'roles': [{
                    'is_admin': user.has_group('base.group_system'),
                    'is_believer': user.has_group('ev_admin.group_rol_believer'),
                }]
            })
        else:
            return json.dumps({
                'status': 'error',
                'message': 'Error retrieving'
            })