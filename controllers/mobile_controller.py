# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from datetime import datetime as dt
import json


class MobileController(http.Controller):

    @http.route('/register/believer', type='json', auth="user", methods=['POST'])
    def RegisterBeliever(self, **post):
        model_believer = request.env['ev.believer']
        model_user = request.env['res.users']

        believer = model_believer.create({
            'name': post.get('name'),
            'from_mobile': True
        })

        model_user.create({
            'login': post.get('email'),
            'password': post.get('password'),
            'partner_id': believer.partner_id.id,
            'believer_id': believer.id
        })

        if believer:
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

    @http.route('/update/believer/<int:believer_id>', type='json', auth="user", methods=['POST'])
    def UpdateBeliever(self, believer_id, **post):
        model_believer = request.env['ev.believer']
        model_user = request.env['res.users']

        believer = model_believer.search([('id', '=', believer_id)])

        if believer:
            believer.write({
                'name': post.get('name'),
                'profile': True,
                'identity': post.get('identity'),
                'state_id': post.get('state_id'),
                'municipality_id': post.get('municipality_id'),
                'parish_id': post.get('parish_id'),
                'sector': post.get('sector'),
                'street': post.get('street'),
                'building': post.get('building'),
                'house': post.get('house'),
                'localphone_number': post.get('localphone_number'),
                'cellphone_number': post.get('cellphone_number')
            })

            user = model_user.search([('believer_id', '=', believer.id)])

            if user:
                if post.get('password'):
                    user.write({
                        'password': post.get('password')
                    })

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

    @http.route('/believers', type='json', auth="user", methods=['GET'])
    def GetBelievers(self, **post):
        model_believer = request.env['ev.believer']
        believers = model_believer.search([('active', '=', True)])

        if believers:
            return json.dumps({
                'status': 'success',
                'message': 'Successfully retrieved',
                'records': [
                    {
                        'id': believer.id,
                        'name': believer.name
                    } for believer in believers
                ]
            })
        else:
            return json.dumps({
                'status': 'error',
                'message': 'Error retrieving'
            })

    @http.route('/believers/<int:believer_id>', type='json', auth="user", methods=['GET'])
    def GetBeliever(self, believer_id, **post):
        model_believer = request.env['ev.believer']
        believer = model_believer.search([('id', '=', believer_id)])

        if believer:
            return json.dumps({
                'status': 'success',
                'message': 'Successfully retrieved',
                'record': {
                    'id': believer.id,
                    'name': believer.name,
                    'identity': believer.identity,
                    'state_id': believer.state_id.id,
                    'municipality_id': believer.municipality_id.id,
                    'parish_id': believer.parish_id.id,
                    'sector': believer.sector,
                    'street': believer.street,
                    'building': believer.building,
                    'house': believer.house,
                    'localphone_number': believer.localphone_number,
                    'cellphone_number': believer.cellphone_number
                }
            })
        else:
            return json.dumps({
                'status': 'error',
                'message': 'Error retrieving'
            })

    @http.route('/departments', type='json', auth="user", methods=['GET'])
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
                        'name': department.name
                    } for department in departments
                ]
            })
        else:
            return json.dumps({
                'status': 'error',
                'message': 'Error retrieving'
            })

    @http.route('/news', type='json', auth="user", methods=['GET'])
    def GetNews(self, **post):
        model_news = request.env['ev.news']
        news = model_news.search([
            ('published', '=', True)
        ], order='date desc')

        if news:
            return json.dumps({
                'status': 'success',
                'message': 'Successfully retrieved',
                'records': [
                    {
                        'id': new.id,
                        'title': new.title,
                        'description': new.description,
                    } for new in news
                ]
            })
        else:
            return json.dumps({
                'status': 'error',
                'message': 'Error retrieving'
            })