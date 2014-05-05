from django.conf.urls import patterns, url

from courses import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^individualSearch/$', views.courseSearch, name='courseSearch'),
    #url(r'^(?P<course_id>\d+)/$', views.course, name='course'),
    #url(r'^findCourse/$',views.singleCourseSearch, name='singleCourseSearch'),
    url(r'^compare/$', views.compare, name='compare'),
    #url(r'^compare/$', views.compare_simple, name='compare'),
    #url(r'^split/$', views.split, name='split'),
    url(r'^advanceSearch/$', views.doSearch, name="doSearch"),
    url(r'^project/$', views.project, name = 'project'),
    url(r'^team/$', views.team, name = 'team'), #replace this with its own view & create template for it too
    url(r'^start/$',views.mainpage, name='mainpage')
)

