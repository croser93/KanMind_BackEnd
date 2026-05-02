from board_app.models import Board
from rest_framework import serializers

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id']