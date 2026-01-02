from django.urls import path
from . import views

urlpatterns = [
    path('', views.QuizView.as_view(), name='quiz'),
    path('list/', views.QuizListView.as_view(), name='quiz-list'),
]