from apscheduler.triggers.cron import CronTrigger
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_apscheduler.models import DjangoJobExecution

from scheduler.serializers import DjangoJobExecutionSerializer
from .jobs import run_spider
from apscheduler.schedulers.base import STATE_STOPPED, STATE_PAUSED
from control.models import Server
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events

scheduler = BackgroundScheduler()

scheduler.add_jobstore(DjangoJobStore(), "default")

# 将 job 中需要的数据提取出来


def job_to_dict(job):
    server_name = Server.objects.get(pk=job.kwargs['id']).name
    return {
        'id': job.id,
        'executor': job.executor,
        'func_ref': job.func_ref,
        'kwargs': job.kwargs,
        'name': job.name,
        'pending': job.pending,
        'next_run_time': job.next_run_time.strftime('%Y年%m月%d日 %H时%M分%S秒'),
        'server_name': server_name,
    }


@api_view()
def get_jobs(request):
    '''
    显示定时任务列表
    '''
    jobs = scheduler.get_jobs()

    data = []

    for item in jobs:
        data.append(job_to_dict(item))
        # return Response(map(job_to_dict, jobs))
    return Response(data)


@api_view()
def get_job(request, id):
    '''
    显示定时任务详细
    '''
    job = scheduler.get_job(id)

    return Response(job_to_dict(job))


@api_view(['POST'])
def add_spider_job(request):
    '''
    添加一个定时任务
    默认使用的是 cron 触发器
    @params id 服务器ID
    '''
    job = scheduler.add_job(run_spider, 'cron',
                            kwargs=request.data,
                            timezone='Asia/Shanghai',
                            **request.data['cron'])
    return Response(job_to_dict(job))


@api_view(['PUT'])
def modify_job(request, id):
    '''
    更新定时任务详细
    '''
    trigger = CronTrigger(**request.data['cron'])
    scheduler.modify_job(id, kwargs=request.data)
    job = scheduler.reschedule_job(
        id, trigger=trigger)

    return Response(job_to_dict(job))


@api_view(['DELETE'])
def remove_job(request, id):
    '''
    删除一个定时任务
    @params id job_id
    '''
    scheduler.remove_job(id)
    return Response()


@api_view()
def status(request):
    '''
    查看定时任务运行状态
    '''

    return Response({
        'status': scheduler.state
    })


@api_view()
def start(request):
    '''
    启动定时任务
    '''
    if scheduler.state == STATE_STOPPED:
        scheduler.start()
    if scheduler.state == STATE_PAUSED:
        scheduler.resume()

    return Response()


@api_view()
def shutdown(request):
    '''
    停止定时任务
    '''
    if scheduler.state != STATE_STOPPED:
        scheduler.shutdown()

    return Response()


@api_view()
def pause(request):
    '''
    暂停定时任务
    '''
    if scheduler.state != STATE_STOPPED:
        scheduler.pause()

    return Response()


@api_view()
def resume(request):
    '''
    重启所有任务
    '''
    if scheduler.state == STATE_STOPPED:
        scheduler.start()
    else:
        scheduler.resume()

    return Response()


@api_view()
def resume_job(request, id):
    '''
    重启任务
    @params id job id
    '''
    scheduler.resume_job(id)

    return Response()


@api_view()
def get_log(request, id):
    '''
    获取日志
    '''
    model = DjangoJobExecution.objects.filter(job_id=id).all()
    logs = DjangoJobExecutionSerializer(model, many=True).data
    return Response(logs)


# 注册定时任务并开始
register_events(scheduler)
scheduler.start()
