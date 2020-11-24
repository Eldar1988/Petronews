from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from questions.functions.q_paginator import get_pagination

from .models import About, Politic, Contacts, Course
from news.models import Post
from news.functions.get_text import get_text

from .tgbot import send_post


def about_view(request):
    """Страница о проекте"""
    about_info = About.objects.last()
    description = get_text(about_info.text)[:170]
    return render(request, 'main/about.html', {'info': about_info, 'description': description})


def politic_view(request):
    """Политика конфиденциальности"""
    politic = Politic.objects.last()
    description = get_text(politic.text)[:170]
    return render(request, 'main/politic.html', {'info': politic, 'description': description})


def contacts_view(request):
    """Конакты"""
    contacts = Contacts.objects.last()
    return render(request, 'main/contacts.html', {'contacts': contacts})


class TgBotView(View):
    """Телеграм бот"""

    def get(self, request):
        posts = Post.objects.filter(public=True, telegram_send=False)
        context = get_pagination(request, posts)
        return render(request, 'main/bot_page.html', context)

    def post(self, request):
        post = Post.objects.get(id=request.POST.get('id'))
        post_url = request.POST.get('tg_url')
        post_url = f'https://petronews.kz{post_url}'

        print(post.id, post_url)
        try:
            send_post(post, post_url)
            post.telegram_send = True
            post.save()
            return HttpResponse('success')
        except:
            status = False
        return HttpResponse('false')


def set_course(request, usd, eur, rub):
    """Обновление курсов"""
    model = Course.objects.last()
    model.usd = round(float(usd), 2)
    model.eur = round(float(eur), 2)
    model.rub = round(float(rub), 2)
    model.save()

    return HttpResponse('success')
