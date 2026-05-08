
from .serializer import BoardSerializer, BoardDetailSerializer, UserSerializer, BoardPatchSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from board_app.models import Board
from django.contrib.auth.models import User
from board_app.api.permissions import IsOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated

class BoardListView(APIView):
    permission_classes = [IsOwnerOrAdmin, IsAuthenticated]
    
    """
    View List for managing Kanban board.
    
    Endpoints:
    - GET /api/boards/ - List all boards where user is a member
    - POST /api/boards/ - Create a new board
    """

    def get(self, request):
            boards = Board.objects.filter(members=request.user)
            serializer = BoardSerializer(boards, many=True)
            return Response(serializer.data, status=200)

    
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
    permission_classes = [IsOwnerOrAdmin, IsAuthenticated]

    """
    Single View for managing board.
    
    Endpoints:
    - GET /api/boards/{ID} - Single board where user is a member
    - PATCH /api/boards/{ID} - Update a signle board
    - DELETE /api/boards/{ID} - Delete a single board
    """

    def get (self, request, pk):
        try:
            board = Board.objects.get(pk = pk)
            self.check_object_permissions(request, board)
            serializer = BoardDetailSerializer(board)
            return Response(serializer.data)
        except Board.DoesNotExist:
            return Response({"error": "Board nicht gefunden. Die angegebene Board-ID existiert nicht."}, status=404)
    
    def patch (self, request, pk):
        try:
            board = Board.objects.get(pk = pk)
            self.check_object_permissions(request, board)
            serializer = BoardPatchSerializer(board, data=request.data, partial=True)
            if serializer.is_valid():
                members = request.data.get('members', None)
                if members is not None:
                    board.members.set(members)
                    board.members.add(board.owner_id)
                serializer.save()
                return Response(serializer.data, status=200)
            return Response({"error": "Ungültige Anfragedaten. Möglicherweise sind einige Anfragen ungültig."}, status=400)
        except Board.DoesNotExist:
             return Response({"error": "Board nicht gefunden. Die angegebene Board-ID existiert nicht."}, status=404)
    
    def delete (self, request, pk):
        try:
            board = Board.objects.get(pk = pk)
            self.check_object_permissions(request, board)
            board.delete()
            return Response(status=204)
        except Board.DoesNotExist:
            return Response({"error": "Board nicht gefunden. Die angegebene Board-ID existiert nicht."}, status=404)

    
class EmailView(APIView):
    permission_classes = [IsOwnerOrAdmin, IsAuthenticated]

    """
    Check is email available
      
    Endpoints:
    - GET /api/email-check/ - Get a email from User
    """

    def get (self, request):
        try:
            email = request.query_params.get('email')
            user = User.objects.filter(email=email).first()
            if user: 
                serializer = UserSerializer(user)
                return Response (serializer.data, status=200)
            return Response ({'error': 'Ungültige Anfrage. Die E-Mail-Adresse fehlt oder hat ein falsches Format'}, status=400)
        except User.DoesNotExist:
            return self.response({'error': 'Email nicht gefunden. Die Email exestiert nicht'}, status=404)

