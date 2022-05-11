import json
from control.models import Server
from bootstrap.testcase import BootstrapTestCase


class ServerTestCase(BootstrapTestCase):
    """
    测试服务器设置的相关操作
    """

    def test_index(self):

        response = self.client.post(
            '/control/servers/', {
                'name': 'default',
                'host': '127.0.0.1',
                'port': 6800,
            })
        self.assertTrue(response.json()['success'])

        response = self.client.get('/control/servers/')
        self.assertTrue(response.json()['success'])

        response = self.client.get('/control/servers/1/')
        self.assertTrue(response.json()['success'])

        response = self.client.patch('/control/servers/1/', {'name': 'put'})
        self.assertTrue(response.json()['success'])

        response = self.client.delete('/control/servers/1/')
        self.assertEquals(len(Server.objects.filter(name='put')), 0)


class ScrapydTestCase(BootstrapTestCase):
    """
    测试scrapyd的相关服务
    没什么好测试的。。
    """

    def setUp(self):
        super().setUp()
        # 创建测试服务，注意测试前应先开启 robot 的 scrapyd 服务
        Server.objects.create(name='default', host='127.0.0.1',
                              port=6800, username='robot', password='robot')

    def test_daemonstatus(self):
        """
        测试获取爬虫服务器状态
        """
        response = self.client.get('/control/daemonstatus/1/')
        self.assertTrue(response.json()['success'])
        self.assertEqual(response.json()['data']['status'], 'ok')

    def test_listprojects(self):
        """
        测试获取爬虫项目列表
        """
        response = self.client.get('/control/listprojects/1/')
        self.assertTrue(response.json()['success'])
        self.assertEqual(response.json()['data']['status'], 'ok')

    def test_schedule(self):
        """
        测试执行一个爬虫任务
        """
        response = self.client.post(
            '/control/schedule/1/', data={
                'project': 'default',
                'spider': '81cn_section'
            })

        self.assertTrue(response.json()['success'])
        self.assertEqual(response.json()['data']['status'], 'ok')
