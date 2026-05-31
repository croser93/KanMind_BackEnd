from django.urls import path
from .views import TaskListView, TaskDetailView, CommentView, CommentDetailView, AssignToMeView, ReviewingView

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='single_task'),
    path('tasks/<int:pk>/comments/', CommentView.as_view(), name='comment_list'),
    path('tasks/<int:task_pk>/comments/<int:comment_pk>/', CommentDetailView.as_view(), name='single_comment'),
    path('tasks/assigned-to-me/', AssignToMeView.as_view(), name='assigned-to-me'),
    path('tasks/reviewing/', ReviewingView.as_view(), name='reviewing'),


]