from django.shortcuts import render
from news.functions.get_text import get_text
from .models import About, Politic, Contacts


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


