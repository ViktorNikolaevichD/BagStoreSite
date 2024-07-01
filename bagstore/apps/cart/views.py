from django.views.generic import TemplateView

class CartPageView(TemplateView):
    '''Отображение корзины'''
    template_name = 'cart.html'
    