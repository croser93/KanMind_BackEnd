from rest_framework import serializers
from task_app.models import CreateTask
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields =['id', 'username', 'email',]

class TaskSerializer (serializers.ModelSerializer):

    assignee_id = UserSerializer(many=True, read_only=True)
    reviewer_id = UserSerializer(read_only=True)
    class Meta:
        model = CreateTask
        fields = '__all__'
