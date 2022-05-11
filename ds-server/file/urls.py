from django.urls import path
from file import views

urlpatterns = [
    path(r'file/tencent_download', views.tencent_download),
    path(r'file/download', views.download_file),
]
