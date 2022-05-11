from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from bootstrap.serializers import UserTokenObtainPairSerializer, UserSerializer
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view()
def userinfo(request):
    '''
    获取用户信息
    '''
    serializer = UserSerializer(request.user)
    return Response(serializer.data)
