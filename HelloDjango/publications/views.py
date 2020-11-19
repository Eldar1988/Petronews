from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View

from .forms import ReviewForm
from .models import Publication, Category, Review
from news.functions.paginator import get_pagination

from news.functions.get_text import get_text


def publications_list_view(request):
    """Список публикаций"""
    publications = Publication.objects.select_related('category').filter(public=True).defer('body', 'update', 'views')
    header = 'Публикации'
    discussed_publications = Publication.objects.defer(
        'body', 'views').filter(public=True).annotate(cnt=Count('reviews')).order_by('-cnt')[:5]
    context = get_pagination(request, publications, header)
    context['discussed_publications'] = discussed_publications
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


def publication_detail_view(request, pk):
    """Дутали публикации"""
    publication = Publication.objects.get(id=pk)
    publications = Publication.objects.defer('body').filter(public=True).exclude(id=pk)[:4]
    description = get_text(publication.body)[:170]
    publication.views += 1
    publication.save()
    comments = Review.objects.filter(publication_id=publication.id)
    comments_count = comments.count()
    return render(request, 'publications/publication_detail.html', {
        'publication': publication,
        'comments': comments,
        'publications': publications,
        'description': description,
        'comments_count': comments_count
    })


class AddPubReview(View):
    """Добавление комментариев"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.publication_id = pk

            if request.user.is_authenticated:
                form.user_id = request.user.id
                print(form.user_id)

            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.save()
            if not request.user.is_authenticated:
                # Создаем имя пользователя в сессии
                if request.session.get('quest_name') is None:
                    request.session['quest_name'] = request.POST.get('name')
                # Создаем Email пользователя в сессии
                if request.session.get('quest_email') is None:
                    request.session['quest_email'] = request.POST.get('email')
                # Переопределяем пользователя в сессии
                if request.session.get('quest_name') != request.POST.get('name'):
                    request.session['quest_name'] = request.POST.get('name')
                if request.session.get('quest_email') != request.POST.get('email'):
                    request.session['quest_email'] = request.POST.get('email')

            return HttpResponse('success')
