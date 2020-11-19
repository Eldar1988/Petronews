from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View


from .functions.paginator import get_pagination
from .models import Post, Category, Review, Notification
from .parsers.parse_starter import parse_starter
from persons.models import Person
from .forms import ReviewForm
from .functions.get_text import get_text
from publications.models import Publication


def home_view(request):
    """Главная страцниа"""
    # Главные новости Казахстана 3
    kz_main_news = Post.objects.select_related(
        'category'
    ).defer(
        'body', 'views', 'source', 'main_source', 'update_date'
    ).filter(
        kz_news=True, main_news=True, public=True)[:5]
    # Главные международные новости
    world_main_news = Post.objects.select_related(
        'category'
    ).defer(
        'body', 'views', 'source', 'main_source', 'update_date'
    ).filter(
        world_news=True,
        main_news=True, public=True)[:5]
    # Новости Казахстана 7
    kz_news = Post.objects.defer(
        'body', 'source', 'main_source', 'update_date', 'image', 'image_url'
    ).filter(
        kz_news=True, main_news=False, public=True)[:25]
    # Межднародные новости 7
    world_news = Post.objects.defer(
        'body', 'source', 'main_source', 'update_date', 'image', 'image_url'
    ).filter(
        world_news=True, main_news=False, public=True)[:25]
    # Актуальные новости
    actual_news = Post.objects.defer('body', 'views', 'source', 'main_source', 'update_date'
                                     ).filter(is_actual=True, public=True)[:9]
    # Персоны 3
    persons = Person.objects.defer('body').all()[:10]
    # Публикации 4
    publications = Publication.objects.select_related(
        'category', 'author'
    ).defer(
        'body', 'views'
    ).filter(public=True).annotate(cnt=Count('reviews')).order_by('-cnt')[:6]
    # 5 самых обсуждаемых новостей
    comments = Post.objects.defer('body', 'views', 'source', 'main_source', 'update_date'
                                     ).filter(public=True).annotate(cnt=Count('reviews')).order_by('-cnt')[:7]
    return render(request, 'news/home.html', {
        'kz_main_news': kz_main_news,
        'world_main_news': world_main_news,
        'kz_news': kz_news,
        'world_news': world_news,
        'actual_news': actual_news,
        'persons': persons,
        'publications': publications,
        'comments': comments
    })


def news_list_view(request):
    """Все новости"""
    news = Post.objects.select_related('category').filter(public=True).defer('body', 'main_source', 'source',
                                                                             'update_date', 'views')
    header = 'Все новости'
    context = get_pagination(request, news, header)
    return render(request, 'news/news_list.html', context)


def kz_news_view(request):
    """Нововсти Казахстана"""
    news = Post.objects.select_related('category').filter(kz_news=True, public=True).defer('body', 'main_source',
                                                                                           'source', 'update_date',
                                                                                           'views')
    header = 'Новости Казахстана'
    context = get_pagination(request, news, header)
    return render(request, 'news/news_list.html', context)


def world_news_view(request):
    """Нововсти мира"""
    news = Post.objects.select_related('category').filter(world_news=True, public=True).defer('body', 'main_source',
                                                                                              'source',
                                                                                              'update_date', 'views')
    header = 'Международные новости'
    context = get_pagination(request, news, header)
    return render(request, 'news/news_list.html', context)


def category_list_view(request, slug):
    """Посты по категории"""
    news = Post.objects.select_related('category').filter(category__slug=slug, public=True).defer('body', 'main_source',
                                                                                              'source',
                                                                                              'update_date', 'views')
    header = Category.objects.get(slug=slug)
    header = header.name
    context = get_pagination(request, news, header)
    return render(request, 'news/news_list.html', context)


def get_search_results(request):
    """вывод результатов поиска"""
    search_request = request.GET.get('s')
    news = Post.objects.select_related('category').filter(title__icontains=search_request).defer('body', 'views')
    pubs = Publication.objects.select_related('category').filter(title__icontains=search_request).defer('body', 'views')
    header = f'Результаты поиска по запросу: "{search_request}"'
    return render(request, 'news/search_results.html', {
        'news': news,
        'header': header,
        'pubs': pubs
    })


def post_detail(request, slug):
    post = Post.objects.get(slug=slug)
    posts = Post.objects.defer('body').filter(public=True).exclude(slug=slug)[:10]
    post.views += 1
    post.save()
    description = get_text(post.body)[:170]
    comments = Review.objects.filter(post_id=post.id)
    comments_count = comments.count()
    return render(request, 'news/post_detail.html', {
        'post': post,
        'comments': comments,
        'posts': posts,
        'description': description,
        'comments_count': comments_count
    })


def parse(request):
    parse_starter()
    return redirect('home')


class AddReview(View):
    """Добавление комментариев"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.post_id = pk

            if request.user.is_authenticated:
                form.user_id = request.user.id

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


def get_404_view(request, exception):
    return render(request, 'error_pages/404.html', {
        'ext': exception
    })


def get_500_view(request):
    return render(request, 'error_pages/500.html', {
    })


def get_403_view(request, exception):
    return render(request, 'error_pages/403.html', {
    })


def get_nots(request):
    """Отчеты парсера"""
    nots = Notification.objects.all()
    return render(request, 'news/parse_nots.html', {'nots': nots})


def clear_nots(request):
    """Отчеты парсера"""
    if request.user.is_authenticated and request.user.is_staff:
        nots = Notification.objects.all()
        for i in nots:
            i.delete()

    return redirect('nots')
