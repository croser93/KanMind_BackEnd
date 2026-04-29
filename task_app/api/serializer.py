from rest_framework import serializers
from task_app.models import CreateTask


class CreateTaskSerializer (serializers.ModelSerializer):

    class Meta:
        model = CreateTask
        fields = '__all__'