import json
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient


class BootstrapTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='ifui', email='ifui@foxmail.com1', password='ifuboy')
        user.save()
        self.user = user

        response = self.client.post(
            '/login/', {'username': 'ifui', 'password': 'ifuboy'})

        self.token = json.loads(response.content)['data']['access_token']

        self.client = APIClient()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                                self.token,  content_type='application/json')
