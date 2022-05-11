from django.urls import path, include
from control import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'control/servers', views.ServerViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'control/daemonstatus/<int:id>/', views.daemonstatus),
    path(r'control/listprojects/<int:id>/', views.listprojects),
    path(r'control/addversion/<int:id>/', views.addversion),
    path(r'control/schedule/<int:id>/', views.schedule),
    path(r'control/cancel/<int:id>/', views.cancel),
    path(r'control/listversions/<int:id>/', views.listversions),
    path(r'control/listspiders/<int:id>/', views.listspiders),
    path(r'control/listjobs/<int:id>/', views.listjobs),
    path(r'control/delversion/<int:id>/', views.delversion),
    path(r'control/delproject/<int:id>/', views.delproject),
    path(r'control/logs/<int:id>/', views.logs),
]
