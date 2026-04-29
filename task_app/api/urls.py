from django.urls import path
from .views import TaskListView, TaskDetailView

urlpatterns = [
    path('task/', TaskListView.as_view(), name='task_list'),
    path('task/<int:pk>/', TaskDetailView, name='single_task'),

]