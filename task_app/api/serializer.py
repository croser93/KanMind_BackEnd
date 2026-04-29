from django.tasks import task
from rest_framework import serializers
from task_app.models import CreateTask
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields =['id', 'username', 'email',]

class TaskSerializer (serializers.ModelSerializer):

    assignee_id = UserSerializer(many=True, required=False)
    reviewer_id = UserSerializer(read_only=True)
    assignee_ids_input = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, write_only=True, source='assignee_id')
    class Meta:
        model = CreateTask
        fields = ['id', 'title', 'description', 'status', 'priority', 'due_date', 'board', 'reviewer_id', 'assignee_id', 'assignee_ids_input']

    def create(self, validated_data):
        assignees = validated_data.pop('assignee_id', [])
        task = CreateTask.objects.create(**validated_data)
        task.assignee_id.set(assignees)
        return task