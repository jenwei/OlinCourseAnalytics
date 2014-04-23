from django.contrib import admin
from courses.models import Course
from courses.models import Metric
# Register your models here.

class MetricInline(admin.TabularInline):
	model = Metric
	extra = 1

class CourseAdmin(admin.ModelAdmin):
	#fields = ['coursetitle', 'courseID']
	list_display = ('coursetitle', 'courseID')
	inlines = [MetricInline] 


admin.site.register(Course, CourseAdmin)
