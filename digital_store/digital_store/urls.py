from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('moderation/', include('moderation.urls')),
    path('review/', include('reviews.urls')),
    path('cart/', include('cart.urls')),
    path('', include('shop.urls')),
]


handler404 = 'core.views.page_not_found'


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
