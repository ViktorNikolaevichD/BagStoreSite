from django.conf.urls.static import static
from django.urls import re_path

from apps.shop import views
from bagstore import settings

urlpatterns = [
    re_path(r'^$', views.ShopPageView.as_view(), name='shop'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
