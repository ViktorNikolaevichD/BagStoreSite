from django.views.generic import TemplateView, ListView
from apps.shop.models import Product

class MainPageView(TemplateView):
    '''Отображение главной страницы'''
    template_name = 'index.html'

class ShopPageView(ListView):
    '''Отображение магазина'''
    model = Product
    template_name = 'shop.html'

    