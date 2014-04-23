from django.db import models

# Create your models here.

class Course(models.Model):
	courseID = models.CharField(max_length=200)
	coursetitle = models.CharField(max_length=200)

	def __unicode__(self):
		return self.coursetitle


class Metric(models.Model):
	course = models.ForeignKey(Course)
	name=models.CharField(max_length=200)
	value = models.CharField(max_length=200)

	def __unicode__(self):
		return self.name
