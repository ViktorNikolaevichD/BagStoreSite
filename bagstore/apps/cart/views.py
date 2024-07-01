from django.views.generic import ListView

from apps.cart.models import Cart

class CartPageView(ListView):
    '''Отображение корзины'''
    model = Cart
    template_name = 'cart.html'
    