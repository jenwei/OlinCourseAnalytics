# -*- coding: utf-8 -*-
"""
Created on Sun May  4 12:31:00 2014

@author: ldavis
"""
from sdfinal.models import Datapoint, Student, Course

def many2many():
    for dp in Datapoint.objects.all():
        student = Student.objects.get(pk=dp.stuid)
        course = Course.objects.get(pk=dp.courseid)    
        dp.student = student
        print student.id
        print "test"
        dp.course = course
        student.courses.add(course)