from .serializer import BoardSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from board_app.models import Board

class BoardListView(APIView):

    def get(self, request):
        boards = Board.objects.all()
        serializer = BoardSerializer(boards, many=True)
        if serializer.is_valid:
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)