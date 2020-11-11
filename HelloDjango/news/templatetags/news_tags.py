from django import template
from ..models import Post

register = template.Library()


@register.inclusion_tag('news/includes/populars.html')
def get_popular_news(post_count):
    popular_news = Post.objects.select_related('category').filter(public=True).order_by('-views').defer(
        'parse_category', 'parse_title', 'body', 'source', 'main_source'
    )[:post_count]
    return {'popular_news': popular_news}
