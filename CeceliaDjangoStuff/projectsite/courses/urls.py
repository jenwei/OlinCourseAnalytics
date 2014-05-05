from django.conf.urls import patterns, url

from courses import views

urlpatterns = patterns('',
    url(r'^$', views.mainpage, name='index'),
    url(r'^advanceSearch/$', views.advanceSearch, name='advanceSearch'),
    #url(r'^(?P<course_id>\d+)/$', views.course, name='course'),
    #url(r'^findCourse/$',views.singleCourseSearch, name='singleCourseSearch'),
    #url(r'^compare/$', views.compare_simple, name='compare'),
    url(r'^compare/$', views.compare, name='compare'),
    #url(r'^split/$', views.split, name='split'),
    url(r'^doSearch/$', views.courseSearch, name="doSearch"),
    url(r'^project/$', views.project, name = 'project'),
    url(r'^team/$', views.team, name = 'team'), #replace this with its own view & create template for it too
    url(r'^start/$',views.mainpage, name='mainpage')
)

