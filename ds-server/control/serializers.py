from rest_framework import serializers
from control.models import Server


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = ('id', 'name', 'host', 'port',
                  'username', 'password', 'to_email')
