# -*- coding: utf-8 -*-
from openerp import http

class OpenAcademy(http.Controller):
    @http.route('/openacademy/openacademy/', auth='public')
    def index(self, **kw):
        Teachers = http.request.env['openacademy.teachers']
        return http.request.render('openacademy.index', {
            'teachers': Teachers.search([])
            })


#        return http.request.render('openacademy.index', {
#           'teachers': ["Diana Padilla", "Jody Caroll", "Lester Vaughn",
#            "Hans Anders", "Spec Savers"],
#                   })
#     @http.route('/openacademy/openacademy/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('openacademy.listing', {
#             'root': '/openacademy/openacademy',
#             'objects': http.request.env['openacademy.openacademy'].search([]),
#         })

#     @http.route('/openacademy/openacademy/objects/<model("openacademy.openacademy"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('openacademy.object', {
#             'object': obj
#         })
