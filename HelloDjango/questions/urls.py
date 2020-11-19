from django.urls import path
from . import views

urlpatterns = [
    path('', views.questions_list, name='questions'),
    path('<int:pk>', views.QuestionDetailView.as_view(), name='question_detail'),
    path('add_question/', views.AddQuestion.as_view(), name='add_question'),
    path('add_answer/<int:pk>', views.AddAnswer.as_view(), name='add_answer'),
]