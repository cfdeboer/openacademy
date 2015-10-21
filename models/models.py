# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Teachers(models.Model):
     _name= "openacademy.teachers"
     _inherit = 'res.partner'
     name = fields.Char(string='Teachers')


class Course(models.Model):
     _name = 'openacademy.course'
     name = fields.Char(string= "Title", required=True)
     description = fields.Text(string="description")
     session_ids=fields.One2many('openacademy.session', 'course_id',
              string="Sessions no.") #, compute='show_session_id')
     attendee_ids=fields.Many2many('openacademy.attendee', 
             string='Course Attendees')
     total_course_sessions=fields.Char(string='total sessions in course',
              compute='calculate_total_sess' )
     average_sess = fields.Char(string= 'average sessions',
              compute='sess_div_courses')
  

     #----called in attr: total_course_sessions
     def calculate_total_sess(self):
         for course in self:
             course.total_course_sessions= len(course.session_ids)


     def sess_div_courses(self):
         all_courses = self.env['openacademy.course'].search_count([])
         all_sessions = self.env['openacademy.session'].search_count([])
         course_average = 1.0*all_sessions/all_courses
         for course in self:
             course.average_sess= course_average

     def veggies(self):
         pass
         #for course in self:
             # ''' veggies_per_course=0
             # attendees = self.env['openacademy.attendee']
             # for attendee in attendees:
             #    if attendee.vegetarian:
             #        veggie_count_per_course += 1'''
          #   course.veggies_per_course = 555  #veggie_count_per_course




class Session(models.Model):
     _name = 'openacademy.session'
     name = fields.Char(string="Session title or no.")
     description = fields.Text()
     duration= fields.Text()
     start_date = fields.Text()
     lunch= fields.Boolean("Vegetarian food available", default=False)
     course_id= fields.Many2one('openacademy.course', string='Course')
     attendee_ids=fields.Many2many('openacademy.attendee', string= 'Session Attendee id')
     teacher_id = fields.Many2one('openacademy.teachers', string="Teacher")
     vegies_per_session = fields.Char(string="vegetarians in session",
          compute='veggies' ) 
  

     # total_vegies= fields.Char('openacademy.attendee.total_vegetarians', 
     
     def veggies(self):
         for session in self:
             print "Session Attendees:", session.attendee_id.attendee_idss
             vegies_count_per_session=0
             attendees = self.env['openacademy.attendee']
             for attendee in attendees:
                print "Attendee:",attendee, "Attendees:",attendees 
                if attendee.vegetarian:
                    vegies_count_per_session += 1
             session.vegies_per_session = vegies_count_per_session




class Attendee(models.Model):
    _name='openacademy.attendee'
    _inherit='res.partner'
    vegetarian = fields.Boolean(string="vegetarian", default=False) 
    attendee_ids=fields.Many2many('res.partner', string= 'Attendee id')
    total_vegetarians= fields.Char(string ="total vegetarians", \
            compute = "count_vegetarians")


    def count_vegetarians(self):
        count = 0
        for attendees in self:
            if (attendees.vegetarian==True):
                count += 1
        # with "total_vegetarians" we fill xml field name  "total vegetarians"        
        for attendees in self:
            attendees.total_vegetarians= count













