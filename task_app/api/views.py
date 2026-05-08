from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsReviewerOrAssigneeOrAdmin
from .serializer import TaskSerializer, CommentsSerializer, AssignedAndReviewedTaskSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from task_app.models import CreateTask, Comments
from rest_framework import serializers
from board_app.models import Board


class TaskListView(APIView):

    permission_classes = [IsAuthenticated]
        
    """
    View List for managing Kanban tasks.
    
    Endpoints:
    - GET /api/tasks/ - List of all tasks 
    - POST /api/tasks/ - Create a new tasks
    """

    def post(self, request):
        board_id = request.data.get('board')
        try:
            board = Board.objects.get(pk=board_id)
        except Board.DoesNotExist:
            return Response({"error": "Board nicht gefunden. Die angegebene Board-ID existiert nicht"}, status=404)
        
        if not board.members.filter(id=request.user.id).exists():
            return Response({"error": "Verboten. Der Benutzer muss Mitglied des Boards sein, um eine Task zu erstellen."}, status=403)
        
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def get(self, request):
        tasks = CreateTask.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response({"message" : "Die Task wurde erfolgreich erstellt", 'data':serializer.data}, status=200)
    

class TaskDetailView(APIView):
        
    permission_classes = [IsReviewerOrAssigneeOrAdmin, IsAuthenticated]
        
    """
    View for a single Kanban tasks in a board.
    
    Endpoints:
    - GET /api/tasks/{ID}/ - a single task where user is a member
    - PATCH /api/tasks/{ID}/ - a single task where user is a member
    - DELETE /api/tasks/{ID}/ - a single task where user is a member
    """
    def get(self, request, pk):
        try:
            tasks = CreateTask.objects.get(pk=pk)
            self.check_object_permissions(request, tasks)
            serializer = TaskSerializer(tasks)
            return Response(serializer.data)
        except CreateTask.DoesNotExist:
                return Response({"error" : "Task nicht gefunden. Die angegebene Task-ID existiert nicht.",}, status=404)
    
    def patch(self, request, pk):
        try:
            tasks = CreateTask.objects.get(pk=pk)
            self.check_object_permissions(request, tasks)
            serializer = TaskSerializer(tasks, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        except CreateTask.DoesNotExist:
                return Response({"error" : "Task nicht gefunden. Die angegebene Task-ID existiert nicht.",}, status=404)
    
    def delete(self, request, pk):
        try:
            tasks = CreateTask.objects.get(pk=pk)
            self.check_object_permissions(request, tasks)
            tasks.delete()
            return Response(status=204)
        except CreateTask.DoesNotExist:
                return Response({"error" : "Task nicht gefunden. Die angegebene Task-ID existiert nicht.",}, status=404)

class CommentView(APIView):
     
    permission_classes = [IsAuthenticated]
        
    """
    View comment list in a tasks for managing in Kanban board.
    
    Endpoints:
    - GET /api/tasks/{ID}/comments/ - List all comments from a Task user is a member
    - POST /api/tasks/{ID}/comments/ - Create a new comment in a Task user is a member
    """
    def get(self, request, pk):
        try:
            task = CreateTask.objects.get(pk=pk)            
        except CreateTask.DoesNotExist:
            return Response({"error": "Task nicht gefunden. Die angegebene Task-ID existiert nicht."}, status=404)
        
        if not task.board.members.filter(id=request.user.id).exists():
            return Response({"error": "Verboten. Der Benutzer muss Mitglied des Boards sein, zu dem die Task gehört."}, status=403)
        comment = Comments.objects.filter(task=pk)
        serializer = CommentsSerializer(comment, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        try:
            task = CreateTask.objects.get(pk=pk)
        except CreateTask.DoesNotExist:
            return Response({"error": "Task nicht gefunden. Die angegebene Task-ID existiert nicht."}, status=404)
        
        if not task.board.members.filter(id=request.user.id).exists():
            return Response({"error": "Verboten. Der Benutzer muss Mitglied des Boards sein, zu dem die Task gehört."}, status=403)
        
        serializer = CommentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(task_id=pk, author=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
class CommentDetailView(APIView):
     
    permission_classes = [IsAuthenticated]
        
    """
    View a signle Comment in a tasks for managing in Kanban board.
    
    Endpoints:
    - GET /api/tasks/{ID}/comments/{ID}/ - Single comments from a Task user is a member
    - DELETE /api/tasks/{ID}/comments/{ID}/ - Delete single comments from a Task user is a member
    """
    def get(self, request, task_pk, comment_pk):
        try:
            comment = Comments.objects.get(task=task_pk, pk=comment_pk)
            if not comment.task.board.members.filter(id=request.user.id).exists():
                return Response({"error": "Verboten. Der Benutzer muss Mitglied des Boards sein, zu dem die Task gehört."}, status=403)
            serializer = CommentsSerializer(comment)
            return Response(serializer.data)
        except Comments.DoesNotExist:
            return Response({"error" : "Kommentar oder Task nicht gefunden.",}, status=404)
    
    def delete(self, request, task_pk, comment_pk):
        try:
            comment = Comments.objects.get(task=task_pk, pk=comment_pk)  
        except Comments.DoesNotExist:
            return Response({"error" : "Kommentar oder Task nicht gefunden.",}, status=404)
        if comment.author != request.user:
            return Response({"error": "Verboten. Der Benutzer muss Mitglied des Boards sein, zu dem die Task gehört.."}, status=403)  
        comment.delete()
        return Response(status=204)

class AssignToMeView(APIView):

    permission_classes = [IsAuthenticated]
        
    """
    View List for tasks from Kanban board User = assigned-to-me .
    
    Endpoints:
    - GET /api/tasks/assigned-to-me/ - List all task where user is assigned-to-me

    """
    def get(self, request):
        tasks = CreateTask.objects.filter(assignee_id=request.user)
        serializer = AssignedAndReviewedTaskSerializer(tasks, many=True)
        return Response(serializer.data, status=200)

class ReviewingView(APIView):

    permission_classes = [IsAuthenticated]
        
    """
    View List for tasks from Kanban board User = reviewing.
    
    Endpoints:
    - GET /api/tasks/reviewing/ - List all task where user is reviewing
    """
    def get(self, request):
        tasks = CreateTask.objects.filter(reviewer_id=request.user)
        serializer = AssignedAndReviewedTaskSerializer(tasks, many=True)
        return Response(serializer.data, status=200)
