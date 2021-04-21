from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from news_site import settings
from .views import home_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name="home_page"),
    path('', include("news_site_news.urls", namespace="news")),
    path('', include("news_site_news_tag.urls", namespace="tags")),
    path('account/', include("news_site_account.urls", namespace="account")),
    path('', include("news_site_news_author.urls", namespace="author")),
    path('gallery/', include("news_site_gallery.urls", namespace="gallery")),
]

handler404 = 'news_site.views.view_404'
handler403 = 'news_site.views.view_403'
handler400 = 'news_site.views.view_400'
handler500 = 'news_site.views.view_500'

if settings.DEBUG:
    # ADD ROOT STATIC FILES
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # ADD MEDIA STATIC FILES
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
