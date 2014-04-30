from django.db import models

# Create your models here.
#dataFileName = 'course_enrollments_2002-2014spring_anonymized.csv'
#dataDictionaries = get_course_data(dataFileName)

class Course(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    name = models.TextField(db_column='Name')
    class Meta:
        managed = False
        db_table = 'Courses'
        
    def __unicode__(self):
		return self.name

class Datapoint(models.Model):
    stuid = models.IntegerField(db_column='StuID')
    gradyear = models.TextField(db_column='GradYear')
    stusem = models.IntegerField(db_column='StuSem')
    stugen = models.TextField(db_column='StuGen')
    stumaj = models.TextField(db_column='StuMaj')
    courseid = models.IntegerField(db_column='CourseID')
    profid = models.IntegerField(db_column='ProfID')
    class Meta:
        managed = False
        db_table = 'Datapoints'
    
    def __unicode__(self):
		return self.stuid, self.courseid

class Student(models.Model):
    id = models.IntegerField(db_column='ID',primary_key=True)
    gradyear = models.IntegerField(db_column='GradYear')
    stugen = models.TextField(db_column='StuGen')
    stumaj = models.TextField(db_column='StuMaj')
    class Meta:
        managed = False
        db_table = 'Students'
    
    def __unicode__(self):
		return self.id
