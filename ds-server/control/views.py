from rest_framework import viewsets
from control.serializers import ServerSerializer
from control.models import Server
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import APIException
import requests


class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer


@api_view()
def daemonstatus(request, id):
    """
    获取指定节点状态
    """
    model = Server.objects.get(pk=id)
    url = 'http://%s:%d/daemonstatus.json' % (model.host, model.port)
    try:
        data = requests.get(url, auth=(model.username, model.password))
        return Response(data.json())
    except:
        raise APIException('服务器连接失败，请检查相关配置')


@api_view(['POST'])
def addversion(request, id):
    """
    Add a version to a project, creating the project if it doesn’t exist.
    """
    model = Server.objects.get(pk=id)
    url = 'http://%s:%d/addversion.json' % (model.host, model.port)

    data = requests.post(url, auth=(
        model.username, model.password), data=request.data)

    return Response(data.json())


@api_view()
def listprojects(request, id):
    """
    获取爬虫项目列表
    """
    model = Server.objects.get(pk=id)

    url = 'http://%s:%d/listprojects.json' % (model.host, model.port)
    data = requests.get(url, auth=(model.username, model.password))

    return Response(data.json())


@api_view(['POST'])
def schedule(request, id):
    """
    执行爬虫

    @params
        - project (string, required) - the project name
        - spider (string, required) - the spider name
        - setting (string, optional) - a Scrapy setting to use when running the spider
        - jobid (string, optional) - a job id used to identify the job, overrides the default generated UUID
        - priority (float, optional) - priority for this project’s spider queue — 0 by default
        - _version (string, optional) - the version of the project to use
    """

    model = Server.objects.get(pk=id)
    url = 'http://%s:%d/schedule.json' % (model.host, model.port)
    data = requests.post(url, auth=(
        model.username, model.password), data=request.data)

    return Response(data.json())


@api_view(['POST'])
def cancel(request, id):
    """
    取消某个任务

    @params
        - project (string, required) - the project name
        - job (string, required) - the job id
    """

    model = Server.objects.get(pk=id)
    url = 'http://%s:%d/cancel.json' % (model.host, model.port)
    data = requests.post(url, auth=(
        model.username, model.password), data=request.data)

    return Response(data.json())


@api_view(['POST'])
def listversions(request, id):
    """
    显示项目版本信息

    @params
        - project (string, required) - the project name
    """

    model = Server.objects.get(pk=id)
    url = 'http://%s:%d/listversions.json' % (model.host, model.port)
    data = requests.get(url, auth=(
        model.username, model.password), params=request.data)

    return Response(data.json())


@api_view(['POST'])
def listspiders(request, id):
    """
    显示项目下的爬虫工程

    @params
        - project (string, required) - the project name
        - _version (string, optional) - the version of the project to examine
    """

    model = Server.objects.get(pk=id)
    url = 'http://%s:%d/listspiders.json' % (model.host, model.port)

    data = requests.get(url, auth=(
        model.username, model.password), params=request.data)

    return Response(data.json())


@api_view(['POST'])
def listjobs(request, id):
    """
    显示爬虫工作状态

    @params
        - project (string, option) - restrict results to project name
    """

    model = Server.objects.get(pk=id)
    url = 'http://%s:%d/listjobs.json' % (model.host, model.port)
    data = requests.get(url, auth=(
        model.username, model.password), data=request.data)

    return Response(data.json())


@api_view(['POST'])
def delversion(request, id):
    """
    删除某个爬虫项目版本

    @params
        - project (string, required) - the project name
        - version (string, required) - the project version
    """

    model = Server.objects.get(pk=id)
    url = 'http://%s:%d/delversion.json' % (model.host, model.port)
    data = requests.post(url, auth=(
        model.username, model.password), data=request.data)

    return Response(data.json())


@api_view(['POST'])
def delproject(request, id):
    """
    删除某个爬虫项目

    @params
        - project (string, required) - the project name
    """

    model = Server.objects.get(pk=id)
    url = 'http://%s:%d/delproject.json' % (model.host, model.port)
    data = requests.post(url, auth=(
        model.username, model.password), data=request.data)

    return Response(data.json())


@api_view(['POST'])
def logs(request, id):
    """
    获取某个爬虫任务的日志
    """
    model = Server.objects.get(pk=id)
    url = 'http://%s:%d/logs/%s/%s/%s.log' % (
        model.host, model.port, request.data['project'], request.data['spider'], request.data['job'])
    data = requests.get(url, auth=(model.username, model.password))
    data.encoding = 'utf-8'

    return Response(data.text)
