from board_app.models import Board
from rest_framework import serializers
from django.contrib.auth.models import User
from task_app.api.serializer import TaskSerializer


class UserSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        return obj.get_full_name()
    
class BoardSerializer(serializers.ModelSerializer):

    member_count= serializers.SerializerMethodField()
    ticket_count= serializers.SerializerMethodField()
    tasks_to_do_count= serializers.SerializerMethodField()
    tasks_high_prio_count= serializers.SerializerMethodField()
    class Meta:
        model = Board
        fields = ['id', 'title', 'member_count', 'ticket_count','tasks_to_do_count', 'tasks_high_prio_count' ,'owner_id']
        extra_kwargs = {
            'owner_id': {'required': False}
        }

    def get_member_count(self, obj):
        return obj.members.count()
    
    def get_ticket_count(self, obj):
        return obj.tasks.count()
    
    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status='to-do').count()
    
    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority='high').count()
    

    
class BoardDetailSerializer(BoardSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta(BoardSerializer.Meta):
        fields = ['id', 'title', 'owner_id', 'members', 'tasks', 'comments_count']
        extra_kwargs = {
            'members': {'required': False}
        }

    def get_comments_count(self, obj):
        return sum(task.comments.count() for task in obj.tasks.all())

    def create (self, validate_data):
        members = validate_data.pop('members', [])
        board = Board.objects.create(**validate_data) 
        board.members.set(members)
        return board
    
    def update(self, instance, validated_data):
        members = validated_data.pop('members', None)
        instance = super().update(instance, validated_data)
        if members is not None:
            instance.members.set(members)
        return instance
    
    def to_representation(self, instance):
            data = super().to_representation(instance)
            data['members'] = UserSerializer(instance.members.all(), many=True).data
            return data


  

    