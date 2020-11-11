from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Post, Review, Notification


admin.site.register(Notification)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'email', 'text', 'post', 'public', 'pub_date')
    list_editable = ('public',)
    search_fields = ('name', 'text', 'email')
    list_filter = ('user',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'slug')
    list_editable = ('order', 'slug')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('parse_title', 'main_source', 'category', 'get_image', 'kz_news', 'world_news', 'main_news', 'is_actual', 'public', 'pub_date')
    list_editable = ('category', 'kz_news', 'world_news', 'main_news', 'is_actual', 'public')
    list_filter = ('public', 'category', 'kz_news', 'world_news', 'main_news', 'is_actual', 'main_source')
    search_fields = ('parse_title', 'title')
    list_per_page = 20
    save_on_top = True

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} height="100"')
        return mark_safe(f'<img src={obj.image_url} height="100"')

    get_image.short_description = 'Изображение'


admin.site.site_title = 'Petronews'
admin.site.site_header = 'Petronews - администрирование'
