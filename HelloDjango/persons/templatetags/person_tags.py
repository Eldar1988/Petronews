from django import template
from ..models import Person


register = template.Library()


@register.simple_tag()
def get_persons():
    persons = Person.objects.all()[:3]
    return persons
