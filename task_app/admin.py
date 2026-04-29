from django.contrib import admin

# Register your models here.
from django.contrib import admin
from task_app.models import Board, CreateTask

admin.site.register(Board)
admin.site.register(CreateTask)