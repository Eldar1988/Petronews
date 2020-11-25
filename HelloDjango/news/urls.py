from django.urls import path

from . import views
from . import apiviews

urlpatterns = [
    path('', views.home_view, name='home'),
    path('category/<slug:slug>', views.category_list_view, name='category_detail'),
    path('news/', views.news_list_view, name='news'),
    path('kz_news/', views.kz_news_view, name='kz_news'),
    path('world_news/', views.world_news_view, name='world_news'),
    path('parse/', views.parse, name='parse'),
    path('post/<slug:slug>', views.post_detail, name='post_detail'),
    path('add_review/<int:pk>', views.AddReview.as_view(), name='add_review'),
    path('search_results/', views.get_search_results, name='search'),
    path('parse_logs/', views.get_nots, name='nots'),
    path('parse_logs/clear', views.clear_nots, name='clear_nots'),

    path('get_kz_main_news/', apiviews.HomeKzMainNewsView.as_view()),
    path('get_kz_list_news/<int:count>', apiviews.HomeKzListNewsView.as_view()),
    path('get_world_main_news/', apiviews.HomeWorldMainNewsView.as_view()),
    path('get_world_list_news/<int:count>', apiviews.HomeWorldListNewsView.as_view()),

    path('clear_posts/', views.clear_not_public_posts, name='clear_posts'),
]