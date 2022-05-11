import requests
from control.models import Server

# 定义一些定时任务的函数


def run_spider(**kwargs):
    '''
    执行爬虫

    @params
        - project (string, required) - the project name
        - spider (string, required) - the spider name
        - setting (string, optional) - a Scrapy setting to use when running the spider
        - jobid (string, optional) - a job id used to identify the job, overrides the default generated UUID
        - priority (float, optional) - priority for this project’s spider queue — 0 by default
        - _version (string, optional) - the version of the project to use
    '''

    model = Server.objects.get(pk=kwargs['id'])
    url = 'http://%s:%d/schedule.json' % (model.host, model.port)
    requests.post(url, auth=(
        model.username, model.password), data=kwargs['form']).json()
