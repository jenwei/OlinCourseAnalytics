from django.conf.urls import patterns, url

from courses import views

urlpatterns = patterns('',
<<<<<<< HEAD
    #url(r'^$', views.index, name='index'),
    url(r'^$', views.graphs, name='graphs'),
    url(r'^individualSearch/$', views.course, name='course'),
    url(r'^(?P<course_id>\d+)/$', views.course, name='course'),
    url(r'^findCourse/$',views.singleCourseSearch, name='singleCourseSearch'),
=======
    url(r'^$', views.index, name='index'),
    url(r'^individualSearch/$', views.courseSearch, name='courseSearch'),
    #url(r'^(?P<course_id>\d+)/$', views.course, name='course'),
    #url(r'^findCourse/$',views.singleCourseSearch, name='singleCourseSearch'),
>>>>>>> d7e4fad24c6e41e12cb8250d276babc4fd95f683
    url(r'^compare/$', views.compare, name='compare'),
    #url(r'^split/$', views.split, name='split'),
    url(r'^advanceSearch/$', views.doSearch, name="doSearch"),
    url(r'^team/$', views.team, name = 'team') #replace this with its own view & create template for it too

)

