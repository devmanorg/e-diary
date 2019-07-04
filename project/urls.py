from django.conf.urls import url

from datacenter import views


urlpatterns = [
    url(r'^$', views.view_classes, name="classes"),
    url(r'^(?P<year>[\w+ ]+)/(?P<letter>[\w+ ]+)$', views.view_class_info, name="class_info"),
    url(r'^(?P<year>[\w+ ]+)/(?P<letter>[\w+ ]+)/schedule/$', views.view_schedule, name="schedule"),
    url(r'^(?P<year>[\w+ ]+)/(?P<letter>[\w+ ]+)/schedule/$', views.view_schedule, name="schedule"),
    url(r'^schoolkid/(?P<schoolkid_id>[\w+ ]+)/$', views.view_schoolkid, name="schoolkid"),
    url(r'^journal/(?P<year>[\w+ ]+)/(?P<letter>[\w+ ]+)/(?P<subject_id>[\w+ ]+)/$', views.view_journal, name="journal"),
]
