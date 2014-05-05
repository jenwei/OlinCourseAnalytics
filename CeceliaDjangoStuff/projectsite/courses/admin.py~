from django.contrib import admin
from sdfinal.models import Student, Course, Datapoint

class DpAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['id']}),
        (None,               {'fields': ['student']}),
        (None,               {'fields': ['course']}),
        (None,               {'fields': ['profid']}),
    ]
    list_display = ('id','student','course','profid')

class StuAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['id']}),
        (None,               {'fields': ['stumaj']}),
        (None,               {'fields': ['stugen']}),
        (None,               {'fields': ['gradyear']}),
        ('Courses', {'fields': ['courses'], 'classes': ['collapse']}),
    ]
    list_display = ('id','stumaj','stugen','gradyear')

class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Course Information', {'fields': ['id', 'name']}),
    ]
    list_display = ('id','name')

admin.site.register(Student, StuAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Datapoint, DpAdmin)
