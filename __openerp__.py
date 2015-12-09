# -*- coding: utf-8 -*-
{
    'name': "Open Academy",

    'summary': """
       Manage trainings 
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'templates.xml',
        'views/openacademy.xml',
        'views/partner.xml',
        'session-reports.xml',
        'course-reports.xml',
        ],
    
    'css': ['static/src/css/openacademy.css'],
    # always loaded
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
