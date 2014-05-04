from django.conf.urls import patterns, url

from courses import views

urlpatterns = patterns('',
    #url(r'^$', views.index, name='index'),
    url(r'^$', views.graphs, name='graphs'),
    url(r'^individualSearch/$', views.course, name='course'),
    url(r'^(?P<course_id>\d+)/$', views.course, name='course'),
    url(r'^findCourse/$',views.singleCourseSearch, name='singleCourseSearch'),
    url(r'^compare/$', views.compare, name='compare'),
    url(r'^split/$', views.split, name='split'),
    url(r'^advanceSearch/$', views.doSearch, name="doSearch"),
    url(r'^team/$', views.index, name = 'team') #replace this with its own view & create template for it too
)

