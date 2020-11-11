from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Publication, Category


admin.site.register(Category)


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('get_image', 'title', 'category', 'author', 'slug', 'public', 'views', 'pub_date')
    list_display_links = ('get_image', 'title')
    list_editable = ('category', 'slug', 'public')
    list_filter = ('category', 'author')
    save_on_top = True
    save_as = True

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} height="100"')

    get_image.short_description = 'Изображение'
