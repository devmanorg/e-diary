from django.urls import path

from datacenter import views

urlpatterns = [
    path('', views.view_classes, name='classes'),
    path('<str:year>/<str:letter>/', views.view_class_info,
        name='class_info'),
    path('<str:year>/<str:letter>/schedule/',
        views.view_schedule, name='schedule'),
    path('schoolkid/<str:schoolkid_id>/', views.view_schoolkid,
        name='schoolkid'),
    path(
        'journal/<str:year>/<str:letter>/<str:subject_id>/',
        views.view_journal,
        name='journal'),
]
