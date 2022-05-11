from rest_framework import serializers
from django_apscheduler.models import DjangoJobExecution


class DjangoJobExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DjangoJobExecution
        fields = ('id', 'status', 'run_time', 'duration',
                  'finished', 'exception', 'traceback', 'job_id')
