from django.urls import path
from .views import TaskListView, TaskDetailView, CommentView

urlpatterns = [
    path('task/', TaskListView.as_view(), name='task_list'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='single_task'),
    path('task/<int:pk>/comments/', CommentView.as_view(), name='comment_list'),

]