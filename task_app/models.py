from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    title = models.CharField(max_length=250)

class CreateTask(models.Model):

    STATUS_CHOICES = [
        ('to-do', 'To DO'),
        ('in-progress', 'In Progress'),
        ('review', 'Review'),
        ('done', ' Done')
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES)
    assignee_id = models.ManyToManyField(User, related_name='assignee_tasks')
    reviewer_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewer_tasks')
    due_date = models.DateField()

