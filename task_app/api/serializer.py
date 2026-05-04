from django.tasks import task
from rest_framework import serializers
from task_app.models import CreateTask, Comments
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields =['id', 'username', 'email',]

class TaskSerializer (serializers.ModelSerializer):
    class Meta:
        model = CreateTask
        fields = ['id', 'title', 'description', 'status', 'priority', 'due_date', 'board', 'reviewer_id', 'assignee_id']
        extra_kwargs = {
            'assignee_id': {'required': False, 'allow_null': True},
            'reviewer_id': {'required': False, 'allow_null': True},
        }


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['assignee_id'] = UserSerializer(instance.assignee_id).data if instance.assignee_id else None
        data['reviewer_id'] = UserSerializer(instance.reviewer_id).data if instance.reviewer_id else None
        return data

class CommentsSerializer(serializers.ModelSerializer):
     
    author = serializers.SerializerMethodField()
    class Meta:
          model = Comments
          fields =['id' , 'author', 'created_at', 'content']

    def get_author(self, obj):
         return obj.author.get_full_name() or "###"