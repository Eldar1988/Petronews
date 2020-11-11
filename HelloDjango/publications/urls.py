from django.urls import path
from . import views

urlpatterns = [
    path('', views.publications_list_view, name='publications_list'),
    path('<slug:slug>', views.publication_detail_view, name='publication_detail'),
    path('category/<slug:slug>', views.publication_category_detail_view, name='publication_category_detail'),
]
