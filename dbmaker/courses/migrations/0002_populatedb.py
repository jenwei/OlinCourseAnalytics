# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from courses.seedcode import OrganizeData

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        datapoints = OrganizeData.createDataPoints()        
        studentarchive = []
        coursearchive = []
        dpid = 0
        for point in datapoints:
            p = orm.Datapoint.objects.create(id=dpid,courseid=point.course,coursename=OrganizeData.courses[point.course],coursetitle=point.coursetitle,stuid=point.stuID,stugen=point.stuGen,stumaj=point.stuMaj,stusem=point.stuSem,gradyear=point.gradYear,profid=point.prof,profname=OrganizeData.professors[point.prof]) 
            p.save()            
            if point.stuID not in studentarchive:
                s = orm.Student.objects.create(id=point.stuID,gradyear=point.gradYear,stugen=point.stuGen,stumaj=point.stuMaj)
                s.save()
                studentarchive.append(point.stuID)
            if point.course not in coursearchive:
                c = orm.Course.objects.create(id=point.course,name=OrganizeData.courses[point.course],title=point.coursetitle)
                c.save()
                coursearchive.append(point.course)
            dpid+=1
        for dp in orm.Datapoint.objects.all():
            student = orm.Student.objects.get(pk=dp.stuid)
            course = orm.Course.objects.get(pk=dp.courseid)
            dp.student = student
            dp.course = course
            student.courses.add(course)
            dp.save()
            student.save()
            course.save()

    def backwards(self, orm):
        "Write your backwards methods here."
        for dp in orm.Datapoint.objects.all():
            dp.delete()
        for stu in orm.Student.objects.all():
            stu.delete()
        for cou in orm.Course.objects.all():
            cou.delete()


    models = {
        u'courses.course': {
            'Meta': {'object_name': 'Course', 'db_table': "'Courses'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'ID'"}),
            'name': ('django.db.models.fields.TextField', [], {'db_column': "'Name'"}),
            'title': ('django.db.models.fields.TextField', [], {'db_column': "'Title'"})
        },
        u'courses.datapoint': {
            'Meta': {'object_name': 'Datapoint', 'db_table': "'Datapoints'"},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': u"orm['courses.Course']", 'blank': 'True'}),
            'courseid': ('django.db.models.fields.IntegerField', [], {'db_column': "'CourseID'"}),
            'coursename': ('django.db.models.fields.TextField', [], {'db_column': "'CourseName'"}),
            'coursetitle': ('django.db.models.fields.TextField', [], {'db_column': "'CourseTitle'"}),
            'gradyear': ('django.db.models.fields.TextField', [], {'db_column': "'GradYear'"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'ID'"}),
            'profid': ('django.db.models.fields.IntegerField', [], {'db_column': "'ProfID'"}),
            'profname': ('django.db.models.fields.TextField', [], {'db_column': "'ProfName'"}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': u"orm['courses.Student']", 'blank': 'True'}),
            'stugen': ('django.db.models.fields.TextField', [], {'db_column': "'StuGen'"}),
            'stuid': ('django.db.models.fields.IntegerField', [], {'db_column': "'StuID'"}),
            'stumaj': ('django.db.models.fields.TextField', [], {'db_column': "'StuMaj'"}),
            'stusem': ('django.db.models.fields.IntegerField', [], {'db_column': "'StuSem'"})
        },
        u'courses.student': {
            'Meta': {'object_name': 'Student', 'db_table': "'Students'"},
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['courses.Course']", 'symmetrical': 'False', 'db_column': "'courses'", 'blank': 'True'}),
            'gradyear': ('django.db.models.fields.IntegerField', [], {'db_column': "'GradYear'"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'ID'"}),
            'stugen': ('django.db.models.fields.TextField', [], {'db_column': "'StuGen'"}),
            'stumaj': ('django.db.models.fields.TextField', [], {'db_column': "'StuMaj'"})
        }
    }

    complete_apps = ['courses']
    symmetrical = True
