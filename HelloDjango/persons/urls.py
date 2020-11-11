from django.urls import path
from . import views

urlpatterns = [
    path('', views.persons_list_view, name='persons_list'),
    path('<slug:slug>', views.persons_detail_view, name='person_detail'),
]
