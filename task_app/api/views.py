from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializer import CreateTaskSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from task_app.models import CreateTask

class TaskListView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CreateTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def get(self, request):
        tasks = CreateTask.objects.all()
        serializer = CreateTaskSerializer(tasks, many=True)
        return Response({"message" : "efolgreich abgerufen", 'data':serializer.data}, status=200)
    

class TaskDetailView():
    pass

