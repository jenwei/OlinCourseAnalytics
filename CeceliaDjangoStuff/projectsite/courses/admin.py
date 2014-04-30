from django.contrib import admin
from courses.models import Student, Course
from courses.models import Metric
# Register your models here.

class StuAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['id']}),
        (None,               {'fields': ['stumaj']}),
        (None,               {'fields': ['stugen']}),
        (None,               {'fields': ['gradyear']}),
    ]
    list_display = ('id','stumaj','stugen','gradyear')

class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Course Information', {'fields': ['id', 'name']}),
    ]
    list_display = ('id','name')

admin.site.register(Student, StuAdmin)
admin.site.register(Course, CourseAdmin)