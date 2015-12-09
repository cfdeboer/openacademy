# -*- coding: utf-8 -*-

from openerp import models,fields,api


class Wizard (models.TransientModel):
    _name= 'openacademy.wizard'

    def _default_sessions(self):
        print self.env['openacademy.session'].browse(self._context.get('active_ids'))
        return self.env['openacademy.session'].browse(self._context.get('active_ids'))


    session_ids = fields.Many2many('openacademy.session',string="Sessions", 
                       required=True, default=_default_sessions)
    attendee_ids = fields.Many2many('openacademy.attendee', string='Attendees')

    def _default_courses(self):
         print self.env['openacademy.course'].browse(self._context.get('active_ids'))
         return self.env['openacademy.course'].browse(self._context.get('active_ids'))


    course_ids = fields.Many2many('openacademy.course',string="Courses", 
                       required=True, default=_default_courses)




    @api.multi
    def subscribe(self):
        for session in self.session_ids:
            session.attendee_ids |= self.attendee_ids
        return {}


    @api.multi
    def add_sessions(self):
        for course in self.course_ids:
            course.session_ids |= self.session_ids
        return {}

