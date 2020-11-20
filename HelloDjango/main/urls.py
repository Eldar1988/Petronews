from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about_view, name='about'),
    path('politic/', views.politic_view, name='politic'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('bot_admin/', views.TgBotView.as_view(), name='telegram'),
]