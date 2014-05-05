# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Course'
        db.create_table('Courses', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True, db_column='ID')),
            ('name', self.gf('django.db.models.fields.TextField')(db_column='Name')),
        ))
        db.send_create_signal(u'courses', ['Course'])

        # Adding model 'Datapoint'
        db.create_table('Datapoints', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True, db_column='ID')),
            ('stuid', self.gf('django.db.models.fields.IntegerField')(db_column='StuID')),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['courses.Student'], blank=True)),
            ('gradyear', self.gf('django.db.models.fields.TextField')(db_column='GradYear')),
            ('stusem', self.gf('django.db.models.fields.IntegerField')(db_column='StuSem')),
            ('stugen', self.gf('django.db.models.fields.TextField')(db_column='StuGen')),
            ('stumaj', self.gf('django.db.models.fields.TextField')(db_column='StuMaj')),
            ('courseid', self.gf('django.db.models.fields.IntegerField')(db_column='CourseID')),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['courses.Course'], blank=True)),
            ('profid', self.gf('django.db.models.fields.IntegerField')(db_column='ProfID')),
        ))
        db.send_create_signal(u'courses', ['Datapoint'])

        # Adding model 'Student'
        db.create_table('Students', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True, db_column='ID')),
            ('gradyear', self.gf('django.db.models.fields.IntegerField')(db_column='GradYear')),
            ('stugen', self.gf('django.db.models.fields.TextField')(db_column='StuGen')),
            ('stumaj', self.gf('django.db.models.fields.TextField')(db_column='StuMaj')),
        ))
        db.send_create_signal(u'courses', ['Student'])

        # Adding M2M table for field courses on 'Student'
        m2m_table_name = db.shorten_name('Students_courses')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('student', models.ForeignKey(orm[u'courses.student'], null=False)),
            ('course', models.ForeignKey(orm[u'courses.course'], null=False))
        ))
        db.create_unique(m2m_table_name, ['student_id', 'course_id'])


    def backwards(self, orm):
        # Deleting model 'Course'
        db.delete_table('Courses')

        # Deleting model 'Datapoint'
        db.delete_table('Datapoints')

        # Deleting model 'Student'
        db.delete_table('Students')

        # Removing M2M table for field courses on 'Student'
        db.delete_table(db.shorten_name('Students_courses'))


    models = {
        u'courses.course': {
            'Meta': {'object_name': 'Course', 'db_table': "'Courses'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'ID'"}),
            'name': ('django.db.models.fields.TextField', [], {'db_column': "'Name'"})
        },
        u'courses.datapoint': {
            'Meta': {'object_name': 'Datapoint', 'db_table': "'Datapoints'"},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': u"orm['courses.Course']", 'blank': 'True'}),
            'courseid': ('django.db.models.fields.IntegerField', [], {'db_column': "'CourseID'"}),
            'gradyear': ('django.db.models.fields.TextField', [], {'db_column': "'GradYear'"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'ID'"}),
            'profid': ('django.db.models.fields.IntegerField', [], {'db_column': "'ProfID'"}),
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