from control.models import Server
from bootstrap.testcase import BootstrapTestCase


class FileTestCase(BootstrapTestCase):

    def test_index(self):
        # response = self.client.post(
        #     '/file/tencent_download', data={
        #         'start_time': '20220217',
        #         'is_overwrite': True
        #     })
        #
        # self.assertTrue(response.json()['success'])

        response = self.client.get(
            '/file/download?start_time=20220217&is_overwrite=true')

        self.assertTrue(response.status_code == 200)
