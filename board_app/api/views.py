from django import tasks

from .serializer import BoardSerializer, BoardDetailSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from board_app.models import Board
from django.contrib.auth.models import User
from task_app.api.permissions import IsRieviewerOrAssigneeOrAdmin
from rest_framework.permissions import IsAuthenticated , AllowAny


class BoardListView(APIView):
    permission_classes = [IsRieviewerOrAssigneeOrAdmin, IsAuthenticated]

    def get(self, request):
        boards = Board.objects.filter(members=request.user)
        serializer = BoardSerializer(boards, many=True)
        if serializer.is_valid:
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            board = serializer.save(owner_id=request.user)
            members = request.data.get('members', [])
            board.members.set(members)
            board.members.add(request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class BoardDetailView(APIView):
    permission_classes = [IsRieviewerOrAssigneeOrAdmin, IsAuthenticated]

    def get (self, request, pk):
        board = Board.objects.get(pk = pk)
        serializer = BoardDetailSerializer(board)
        return Response(serializer.data)
    
    def patch (self, request, pk):
        self.check_object_permissions(request, tasks)
        board = Board.objects.get(pk = pk)
        serializer = BoardDetailSerializer(board, data=request.data, partial=True)
        if serializer.is_valid():
            members = request.data.get('members', None)
            if members is not None:
                board.members.set(members)
                board.members.add(board.owner_id)
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def delete (self, request, pk):
        self.check_object_permissions(request, tasks)
        board = Board.objects.get(pk = pk)
        board.delete()
        return Response({"message" : "successfully deleted",}, status=204)
    
class EmailView(APIView):
    permission_classes = [IsRieviewerOrAssigneeOrAdmin, IsAuthenticated]

    def get (self, request):
        email = request.query_params.get('email')
        user = User.objects.filter(email=email).first()
        if user: 
            serializer = UserSerializer(user)
            return Response (serializer.data, status=200)
        return Response ({'error': 'User not found'}, status=404)

