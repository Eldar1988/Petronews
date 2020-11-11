from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('get_image', 'name', 'position', 'company', 'slug', 'order')
    list_editable = ('position', 'company', 'slug', 'order')
    list_display_links = ('get_image', 'name')
    save_as = True
    save_on_top = True

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} height="100"')
        return mark_safe(f'<img src="" height="100"')

    get_image.short_description = 'Фото'
