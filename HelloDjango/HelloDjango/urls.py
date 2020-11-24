import debug_toolbar
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
    path('persons/', include('persons.urls')),
    path('publications/', include('publications.urls')),
    path('questions/', include('questions.urls')),
    path('info/', include('main.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('user/', include('profiles.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]

handler404 = 'news.views.get_404_view'
handler500 = 'news.views.get_500_view'
handler403 = 'news.views.get_403_view'

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
