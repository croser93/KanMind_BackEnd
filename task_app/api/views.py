from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from auth_app.api import serializers
from .permissions import IsRieviewerOrAssigneeOrAdmin
from .serializer import TaskSerializer, CommentsSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from task_app.models import CreateTask, Comments
from rest_framework import serializers


class TaskListView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def get(self, request):
        tasks = CreateTask.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response({"message" : "successfully retrieved", 'data':serializer.data}, status=200)
    

class TaskDetailView(APIView):
        
        permission_classes = [IsRieviewerOrAssigneeOrAdmin, IsAuthenticated]

        def get(self, request, pk):
            tasks = CreateTask.objects.get(pk=pk)
            serializer = TaskSerializer(tasks)
            return Response(serializer.data)
        
        def patch(self, request, pk):
            tasks = CreateTask.objects.get(pk=pk)
            self.check_object_permissions(request, tasks)
            serializer = TaskSerializer(tasks, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        
        def delete(self, request, pk):
                tasks = CreateTask.objects.get(pk=pk)
                self.check_object_permissions(request, tasks)
                tasks.delete()
                return Response({"message" : "successfully deleted",}, status=204)

class CommentView(APIView):
     
    permission_classes = [IsRieviewerOrAssigneeOrAdmin, IsAuthenticated]

    def get(self, request, pk):
            comment = Comments.objects.filter(task=pk)
            serializer = CommentsSerializer(comment, many=True)
            return Response(serializer.data)
    
    def post(self, request, pk):
            serializer = CommentsSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save(task_id=pk, author=request.user)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
     
class CommentDetailView(APIView):
     
    permission_classes = [IsRieviewerOrAssigneeOrAdmin, IsAuthenticated]

    def get(self, request, task_pk, comment_pk):
        comment = Comments.objects.get(task=task_pk, pk=comment_pk)
        serializer = CommentsSerializer(comment)
        return Response(serializer.data)
    
    def delete(self, request, task_pk, comment_pk):
        comment = Comments.objects.get(task=task_pk, pk=comment_pk)  
        comment.delete()
        return Response({"message" : "successfully deleted",}, status=204)
    

class AssignToMeView(APIView):

    permission_classes = [IsRieviewerOrAssigneeOrAdmin, IsAuthenticated]
    def get(self, request):
        tasks = CreateTask.objects.filter(assignee_id=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=200)


class ReviewingView(APIView):

    permission_classes = [IsRieviewerOrAssigneeOrAdmin, IsAuthenticated]
    def get(self, request):
        tasks = CreateTask.objects.filter(reviewer_id=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=200)
