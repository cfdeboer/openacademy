# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions

class Teachers(models.Model):
     _name= "openacademy.teachers"
     partner_id=fields.Many2one('res.partner', string='Teacher id', required=False)
# next statment inhibits Administrator from making new contacts
#     _inherit = 'res.partner'
     name = fields.Char(string='Teachers')
     session_ids=fields.One2many('openacademy.session', 
             'teacher_id', string='Sessions to teach' )
     session_amount = fields.Integer(string="Number of sessions",compute="number_of_sessions")
     age = fields.Integer("Age", required=False)

     @api.constrains('age')
     # @api.one
     def constrain_age(self):
         if self.age <= 20:
            raise exceptions.ValidationError(
                    ("Age of teacher must be at least 21!"))
     
     def number_of_sessions(self):
         for teacher in self:
             teacher.session_amount = len(teacher.session_ids)

     #@api.constrains('session_amount')
     #def constrain_session_amount(self):
     #    if self.session_amount < 2:
     ##       raise exceptions.ValidationError("More Sessions please")



class Course(models.Model):
     _name = 'openacademy.course'
     _order = 'session_ids'
     name = fields.Char(string= "Title", required=True)
     description = fields.Text(string="description")
     session_ids=fields.One2many('openacademy.session', 'course_id',
             string="Sessions no.") 
     sessions_list=fields.Char(string='session list',
             compute='list_the_sessions')
     attendee_ids=fields.Many2many('openacademy.attendee','name', 
             string='Course Attendees' )
     attendee_list=fields.Char(string='Course Attendee list: ', 
             compute='list_the_attendees')
     total_course_sessions=fields.Char(string='total sessions in course',
             compute='calculate_total_sess' )
     average_sess = fields.Char(string= 'average sessions',
              compute='sess_div_courses')
     teacher_names= fields.Char(string="Course Teachers", 
             compute='list_the_teachers' )

#     @api.multi
#     def copy(self, default=None):
#         default = dict(default or {})
#         copied_count = self.search_count(
#                 [('name', '=like', u"Copy of {}%".format(self.name))])
#         if not copied_count:
#             new_name = u"Copy of {}".format(self.name)
#         else:
#             new_name = u"Copy of {} ({})".format(self.name, copied_count)
#         default['name'] = new_name
#         return super(Course, self).copy(default)

     
#     _sql_constraints = [ ('name_description_check',
#                           'CHECK(name != description)',
#                           "The title of the course should not be the description"),
##
#                          ('name_unique',
#                           'UNIQUE(name)',
#                           "The course title must be unique"),
#                            ]
#

     @api.constrains('attendee_ids')
     def constrain_attendee(self):
         message=["Attendees can subscribe to a session, not a course, or the world turns to chaos!"]
         for course in self:
             for attendee in self.attendee_ids:
                 if attendee.name:
                    raise exceptions.ValidationError(message[0])
    
     
     def calculate_total_sess(self):
         for course in self:
             course.total_course_sessions= len(course.session_ids)


     def sess_div_courses(self):
         all_courses = self.env['openacademy.course'].search_count([])
         all_sessions = self.env['openacademy.session'].search_count([])
         course_average = 1.0*all_sessions/all_courses
         #print "all courses: ", all_courses, "  all sessions: ", all_sessions
         for course in self:
             course.average_sess= course_average

     def list_the_teachers(courses):
         for course in courses:
             course_teachers_list=[]
             for session_id in course.session_ids:
                 for teacher_id in session_id:
                     teacher_name = session_id.teacher_id.name
                     if teacher_name and teacher_name not in course_teachers_list:
                        # print "Session: ",session_id.name ,", teacher name: ", teacher_name
                        course_teachers_list.append(teacher_name)
             course_teachers_string=str( ', '.join(course_teachers_list))
             course.teacher_names=course_teachers_string

     def list_the_sessions(courses):
          for course in courses:
             course_session_list=[]
             for session_id in course.session_ids:
                 if session_id.name:
                    # print "Session: ",session_id.name 
                    course_session_list.append(session_id.name)
                    # print "Course_session_list: ", course_session_list
             course_session_string = str( ', '.join(course_session_list))
                 # print course_session_string
             course.sessions_list = course_session_string
       
     def list_the_attendees(courses):
         for course in courses:
             course_attendee_list=[]
             for session_id in course.session_ids:
                 for attendee in session_id.attendee_ids:
                     attendee_name= attendee.name
                     if attendee_name not in course_attendee_list:
                        #print "In course: "+ attendee_name
                        course_attendee_list.append(attendee_name)
             course_attendee_string=str(', '.join(course_attendee_list))
             course.attendee_list=course_attendee_string


class Session(models.Model):
     _name = 'openacademy.session'
     name = fields.Char(string="Session title or no.")
     description = fields.Text(string='Session name', required=False)
     duration = fields.Float(digits=(6, 2), help="Duration in days")
     start_date = fields.Date(default=fields.Date.today)
     lunch= fields.Boolean("Vegetarian food available", default=False)
     course_id= fields.Many2one('openacademy.course',  string='Course')
     attendee_ids=fields.Many2many('openacademy.attendee','attendee_ids', 
             string= 'Session Attendee id')
     teacher_id = fields.Many2one('openacademy.teachers', string="Teacher")
     vegies_per_session = fields.Char(string="vegetarians in session",
          compute='veggies' ) 
     attendees_per_session= fields.Char(string= "Attendees per session",
                    compute='num_attendees')
     attendee_list=fields.Char(string='Session attendee list: ', 
             compute='list_the_attendees')
     color = fields.Integer()
     
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

     def list_the_attendees(sessions):
         for session in sessions:
             session_attendee_list=[]
             for attendee in session.attendee_ids:
                     attendee_name= attendee.name
                     if attendee_name and attendee_name not in session_attendee_list:
                        #print "in session: "+attendee_name
                        session_attendee_list.append(attendee_name)
             session_attendee_string=str(', '.join(session_attendee_list))
             session.attendee_list=session_attendee_string


class Attendee(models.Model):
    _name='openacademy.attendee'
    #partner_id=fields.Many2one('res.partner', string='Attendee id', required=False)
     # next statment inhibits Administrator from making new contacts
     #     _inherit = 'res.partner'
    name = fields.Char(string='Attendee')
    vegetarian = fields.Boolean(string="vegetarian", default=False) 
    attendee_ids=fields.Many2many('res.partner', 
            string= 'Attendee id')
    attendee_id_info=fields.Char(string="ID", compute="attendee_info")
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


    def attendee_info(self):
        for attendee in self:
            name = ""
            idname=attendee.attendee_ids.name
            if idname:
                name=idname 
            else:
               name="No id"
            attendee.attendee_id_info=name
               











