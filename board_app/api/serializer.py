from board_app.models import Board
from rest_framework import serializers
from django.contrib.auth.models import User
from task_app.api.serializer import TaskSerializer


class BoardSerializer(serializers.ModelSerializer):

    member_count= serializers.SerializerMethodField()
    ticket_count= serializers.SerializerMethodField()
    tasks_to_do_count= serializers.SerializerMethodField()
    tasks_high_prio_count= serializers.SerializerMethodField()
    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', "member_count", "ticket_count", "tasks_to_do_count", "tasks_high_prio_count"]


    def get_member_count(self, obj):
        return obj.members.count()
    
    def get_ticket_count(self, obj):
        return obj.tasks.count()
    
    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status='to-do').count()
    
    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority='high').count()
    
class MemberSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        return obj.get_full_name() or '####'
    
class BoardDetailSerializer(BoardSerializer):
    members = MemberSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta(BoardSerializer.Meta):
        fields = BoardSerializer.Meta.fields + ['members', 'tasks']


  

    