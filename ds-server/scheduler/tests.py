import json
from bootstrap.testcase import BootstrapTestCase


class SchedulerTestCase(BootstrapTestCase):
    '''
    测试定时器相关功能
    '''

    def test_index(self):
        '''
        测试创建一个定时任务
        '''
        # 创建一个定时任务
        response = self.client.post('/scheduler/add_spider_job/1/', {
            'minute': '3',
        })
        self.assertTrue(response.json()['success'])

        # 获取 job id
        jobId = json.loads(response.json()['data'])['id']

        # 显示定时任务列表
        response = self.client.get('/scheduler/get_jobs/')
        self.assertTrue(response.json()['success'])

        # 显示一个任务的详细
        response = self.client.get('/scheduler/get_job/' + jobId + '/')
        self.assertTrue(response.json()['success'])

        # 更新一个任务
        response = self.client.put('/scheduler/modify_job/' + jobId + '/', {
            'minute': '1'
        })
        self.assertTrue(response.json()['success'])

        # 启动定时任务
        response = self.client.get('/scheduler/start/')
        self.assertTrue(response.json()['success'])

        # 暂停定时任务
        response = self.client.get('/scheduler/pause/')
        self.assertTrue(response.json()['success'])

        # 重启指定定时任务
        response = self.client.get('/scheduler/resume_job/' + jobId + '/')
        self.assertTrue(response.json()['success'])

        # 重启所有定时任务
        response = self.client.get('/scheduler/resume/')
        self.assertTrue(response.json()['success'])

        # 删除一个定时任务
        response = self.client.delete('/scheduler/remove_job/' + jobId + '/')
        self.assertTrue(response.json()['success'])

        # 停止定时任务
        response = self.client.get('/scheduler/shutdown/')
        self.assertTrue(response.json()['success'])
