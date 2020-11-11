from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PostListSerializer
from .models import Post


class HomeKzMainNewsView(APIView):
    """Список главных новостей Казахстана"""
    def get(self, request):
        news = Post.objects.select_related('category').filter(
            kz_news=True, public=True, main_news=True).defer(
            'body', 'main_source', 'source', 'update_date', 'views')[:5]
        serializer = PostListSerializer(news, many=True)
        return Response(serializer.data)


class HomeKzListNewsView(APIView):
    """Список главных новостей Казахстана"""
    def get(self, request, count):
        news = Post.objects.select_related('category').filter(
            kz_news=True, public=True).defer(
            'body', 'main_source', 'source', 'update_date', 'image', 'image_url')[:count]
        serializer = PostListSerializer(news, many=True)
        return Response(serializer.data)


class HomeWorldMainNewsView(APIView):
    """Список главных новостей Казахстана"""
    def get(self, request):
        news = Post.objects.select_related('category').filter(
            world_news=True, public=True, main_news=True).defer(
            'body', 'main_source', 'source', 'update_date', 'views')[:5]
        serializer = PostListSerializer(news, many=True)
        return Response(serializer.data)


class HomeWorldListNewsView(APIView):
    """Список главных новостей Казахстана"""
    def get(self, request, count):
        news = Post.objects.select_related('category').filter(
            world_news=True, public=True).defer(
            'body', 'main_source', 'source', 'update_date', 'views')[:count]
        serializer = PostListSerializer(news, many=True)
        return Response(serializer.data)