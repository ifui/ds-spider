from django.urls import path
from scheduler import views

urlpatterns = [
    path(r'scheduler/get_jobs/', views.get_jobs),
    path(r'scheduler/get_job/<str:id>/', views.get_job),
    path(r'scheduler/modify_job/<str:id>/', views.modify_job),
    path(r'scheduler/add_spider_job/', views.add_spider_job),
    path(r'scheduler/remove_job/<str:id>/', views.remove_job),
    path(r'scheduler/start/', views.start),
    path(r'scheduler/status/', views.status),
    path(r'scheduler/shutdown/', views.shutdown),
    path(r'scheduler/pause/', views.pause),
    path(r'scheduler/resume/', views.resume),
    path(r'scheduler/resume_job/<str:id>/', views.resume_job),
    path(r'scheduler/get_log/<str:id>/', views.get_log),
]
