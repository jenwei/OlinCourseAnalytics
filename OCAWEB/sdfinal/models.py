from django.db import models

#models go below here

class Course(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    name = models.TextField(db_column='Name')
    class Meta:
        db_table = 'Courses'
        
    def __unicode__(self):
		return str(self.name)

class Datapoint(models.Model):
    id = models.IntegerField(db_column='ID',primary_key=True)
    stuid = models.IntegerField(db_column='StuID')
    student = models.ForeignKey('Student', blank=True, default=0)
    gradyear = models.TextField(db_column='GradYear')
    stusem = models.IntegerField(db_column='StuSem')
    stugen = models.TextField(db_column='StuGen')
    stumaj = models.TextField(db_column='StuMaj')
    courseid = models.IntegerField(db_column='CourseID')
    course = models.ForeignKey('Course', blank=True, default=0)
    profid = models.IntegerField(db_column='ProfID')
    class Meta:
        db_table = 'Datapoints'
    
    def __unicode__(self):
		return str(self.stuid)+', '+str(self.courseid)

class Student(models.Model):
    id = models.IntegerField(db_column='ID',primary_key=True)
    gradyear = models.IntegerField(db_column='GradYear')
    stugen = models.TextField(db_column='StuGen')
    stumaj = models.TextField(db_column='StuMaj')
    courses = models.ManyToManyField(Course, db_column='courses', blank=True)
    class Meta:
        db_table = 'Students'
    
    def __unicode__(self):
		return str(self.id)
  
