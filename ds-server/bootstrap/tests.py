
from bootstrap.testcase import BootstrapTestCase
import json


class AuthTestCase(BootstrapTestCase):

    def test_userinfo(self):
        """
        获取用户信息测试
        """
        response = self.client.get('/userinfo/')
        self.assertTrue(response.json()['success'])
