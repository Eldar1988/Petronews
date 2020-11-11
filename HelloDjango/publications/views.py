from django.shortcuts import render

from .models import Publication, Category, Review
from news.functions.paginator import get_pagination

from news.functions.get_text import get_text


def publications_list_view(request):
    """Список публикаций"""
    publications = Publication.objects.select_related('category').filter(public=True).defer('body', 'update', 'views')
    header = 'Все публикации'
    context = get_pagination(request, publications, header)
    return render(request, 'publications/publications_list.html', context)


def publication_category_detail_view(request, slug):
    """Детали публикации"""
    publications = Publication.objects.select_related('category').filter(category__slug=slug, public=True).defer('body',
                                                                                                  'update_date',
                                                                                                  'views')
    header = Category.objects.get(slug=slug)
    header = header.name
    context = get_pagination(request, publications, header)
    return render(request, 'publications/publications_list.html', context)


def publication_detail_view(request, slug):
    """Дутали публикации"""
    publication = Publication.objects.get(slug=slug)
    publications = Publication.objects.defer('body').filter(public=True).exclude(slug=slug)[:4]
    description = get_text(publication.body)[:170]
    publication.views += 1
    publication.save()
    comments = Review.objects.filter(publication_id=publication.id)
    comments_count = comments.count()
    return render(request, 'publications/publications_detail.html', {
        'publication': publication,
        'comments': comments,
        'publications': publications,
        'description': description,
        'comments_count': comments_count
    })