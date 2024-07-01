from django.test import TestCase
from django.urls import reverse

class CartPageTest(TestCase):
    '''Тест страницы магазина'''

    def test_cart_page_template(self):
        '''Тест: используется шаблон для страницы корзины'''
        response = self.client.get(reverse('cart'))
        
        self.assertTemplateUsed(response, 'cart.html')
        