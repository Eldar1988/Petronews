from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('get_image', 'first_name', 'last_name', 'user')
    list_display_links = ('get_image', 'last_name', 'first_name')

    def get_image(self, obj):
        if obj.avatar:
            return mark_safe(f'<img src={obj.avatar.url} height="100"')


    get_image.short_description = 'Аватар'
