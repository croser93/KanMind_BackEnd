from django.contrib import admin

# Register your models here.
from django.contrib import admin
from task_app.models import  CreateTask, Comments


admin.site.register(CreateTask)
admin.site.register(Comments)