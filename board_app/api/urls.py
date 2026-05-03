from django.urls import path
from .views import BoardListView, BoardDetailView, EmailView

urlpatterns = [
    path('boards/', BoardListView.as_view(), name='board-list'),
    path('boards/<int:pk>/', BoardDetailView.as_view(), name='board-detail'),
    path('email-check/', EmailView.as_view(), name='email-check'),
]