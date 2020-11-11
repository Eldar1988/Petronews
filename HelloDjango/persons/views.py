from django.shortcuts import render
from .models import Person
from news.functions.get_text import get_text


def persons_list_view(request):
    """Список персон"""
    persons = Person.objects.defer('body').all()
    return render(request, 'persons/persons_list.html', {
        'persons': persons,
    })


def persons_detail_view(request, slug):
    """Список персон"""
    person = Person.objects.get(slug=slug)
    persons = Person.objects.exclude(slug=slug)[:8]
    description = get_text(person.body)[:170]
    return render(request, 'persons/person_detail.html', {
        'person': person,
        'description': description,
        'persons': persons
    })
