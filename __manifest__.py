# -*- coding: utf-8 -*-
{
    'name': "ev admin",
    'summary': """
        Admin for living hope (Esperanza Viva) app.
    """,
    'description': """
        EV admin module.
    """,
    'author': "yusuke1998",
    'category': 'app',
    'version': '0.1',
    'depends': ['base', 'portal', 'website', 'address_venezuela'],
    'data': [
        # seeds
        'data/departments.xml',

        # security
        'security/ev_roles.xml',
        'security/admin/ir.model.access.csv',
        'security/believer/ir.model.access.csv',

        # menu
        'views/menu_top.xml',
        
        # views
        'views/believer.xml',
        'views/department.xml',
        'views/new.xml',
    ],
    'installable': True,
    'demo': [
        'demo/demo.xml',
    ],
}
