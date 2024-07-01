from django.conf.urls.static import static
from django.urls import re_path

from apps.cart import views
from bagstore import settings

urlpatterns = [
    re_path(r'^$', views.CartPageView.as_view(), name='cart'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
