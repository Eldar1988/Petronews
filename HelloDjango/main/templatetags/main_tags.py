from django import template
from ..models import Social, MainInfo, Footer, Course

register = template.Library()


@register.simple_tag()
def get_main_info():
    main_info = MainInfo.objects.last()
    return main_info


@register.simple_tag()
def get_socials():
    socials = Social.objects.all()
    return socials


@register.simple_tag()
def get_footer_info():
    footer = Footer.objects.last()
    return footer


@register.simple_tag()
def get_course():
    course = Course.objects.last()
    return course
