# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Teachers(models.Model):
     _name= "openacademy.teachers"
     _inherit = 'res.partner'
     name = fields.Char(string='Teachers')
     session_ids=fields.One2many('openacademy.session', 
             'teacher_id', string='Sessions to teach' )


class Course(models.Model):
     _name = 'openacademy.course'
     name = fields.Char(string= "Title", required=True)
     description = fields.Text(string="description")
     session_ids=fields.One2many('openacademy.session', 'course_id',
              string="Sessions no.") 
     attendee_ids=fields.Many2many('openacademy.attendee', 
             string='Course Attendees')
     total_course_sessions=fields.Char(string='total sessions in course',
              compute='calculate_total_sess' )
     average_sess = fields.Char(string= 'average sessions',
              compute='sess_div_courses')
     
     
     def calculate_total_sess(self):
         for course in self:
             course.total_course_sessions= len(course.session_ids)


     def sess_div_courses(self):
         all_courses = self.env['openacademy.course'].search_count([])
         all_sessions = self.env['openacademy.session'].search_count([])
         course_average = 1.0*all_sessions/all_courses
         for course in self:
             course.average_sess= course_average

class Session(models.Model):
     _name = 'openacademy.session'
     name = fields.Char(string="Session title or no.")
     description = fields.Text(string='Session name', required=True)
     duration= fields.Text()
     start_date = fields.Text()
     lunch= fields.Boolean("Vegetarian food available", default=False)
     course_id= fields.Many2one('openacademy.course', string='Course')
     attendee_ids=fields.Many2many('openacademy.attendee', 
             string= 'Session Attendee id')
     teacher_id = fields.Many2one('openacademy.teachers', string="Teacher")
     vegies_per_session = fields.Char(string="vegetarians in session",
          compute='veggies' ) 
     attendees_per_session= fields.Char(string= "Attendees per session",
                    compute='num_attendees')

     
     def veggies(self):
         for session in self:
             vegies_count_per_session=0
             for attendee in session.attendee_ids:
                if attendee.vegetarian:
                    vegies_count_per_session += 1
             session.vegies_per_session = vegies_count_per_session

     #--number of attendees er session
     def num_attendees(self):
         for session in self:
             count_session_attendees=0
             for attendee in session.attendee_ids:
                 count_session_attendees += 1
             session.attendees_per_session=count_session_attendees


class Attendee(models.Model):
    _name='openacademy.attendee'
    _inherit='res.partner'
    vegetarian = fields.Boolean(string="vegetarian", default=False) 
    attendee_ids=fields.Many2many('res.partner', string= 'Attendee id')
    total_vegetarians= fields.Char(string ="total vegetarians", \
            compute = "count_vegetarians")
    sessions= fields.Many2many('openacademy.session','attendee_ids', 
            string='Participates in session:')

    def count_vegetarians(self):
        count = 0
        for attendees in self:
            if (attendees.vegetarian==True):
                count += 1
        for a in self:
            a.total_vegetarians= count













