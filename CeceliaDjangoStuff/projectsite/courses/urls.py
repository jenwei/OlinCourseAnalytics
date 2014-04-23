from django.conf.urls import patterns, url

from courses import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<course_id>\d+)/$', views.course, name='course'),
    url(r'^compare/$', views.compare, name='compare'),
    url(r'^split/$', views.split, name='split')
)