from django.db import models
from django.contrib.auth.models import User

class Board(models.Model):
    title = models.CharField(max_length=255)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="boards")

    def __str__(self):
        return self.title