from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from bootstrap.views import UserTokenObtainPairView
from rest_framework.routers import DefaultRouter
from bootstrap import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('login/', UserTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('userinfo/', views.userinfo),
    path(r'', include(router.urls))
]
