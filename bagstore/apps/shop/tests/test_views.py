import os

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from apps.cart.models import Cart
from apps.shop.models import Product


User = get_user_model()


class MainPageTest(TestCase):
    '''Тест главной страницы'''

    def test_main_page_template(self):
        '''Тест: используется шаблон для главной страницы'''
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'index.html')
    

class ShopPageTest(TestCase):
    '''Тест страницы магазина'''

    def setUp(self):
        '''Установка перед тестированием'''  
        self.image = SimpleUploadedFile(
            name='test_first_image.jpg',
            content=open(
                'bagstore/media_for_tests/woman.png', 'rb').read(),
            content_type='image/jpeg'
        )
    
    def tearDown(self):
        '''Удаление параметров тестирования'''
        for product in Product.objects.all():
            if product is not None:
                os.remove(product.image.path)

    def test_shop_page_template(self):
        '''Тест: используется шаблон для страницы магазина'''
        response = self.client.get(reverse('shop'))
        
        self.assertTemplateUsed(response, 'shop.html')
    
    def test_all_products_are_passed_to_the_shop_template(self):
        '''Тест: в шаблон магазина передаются все продукты'''
        Product.objects.create(
            name="Сумка 1",
            price=1250,
            image=self.image
        )
        Product.objects.create(
            name="Сумка 2",
            price=1250,
            image=self.image
        )
        products = Product.objects.all()
        response = self.client.get(reverse('shop'))
        self.assertEqual(list(response.context['product_list']), list(products))

    def test_all_products_are_displayed_in_the_shop_template(self):
        '''Тест: в шаблоне магазина отображаются все продукты'''
        Product.objects.create(
            name="Сумка 1",
            price=1250,
            image=self.image
        )
        Product.objects.create(
            name="Сумка 2",
            price=1250,
            image=self.image
        )
        response = self.client.get(reverse('shop'))

        self.assertContains(response, 'Сумка 1')
        self.assertContains(response, 'Сумка 2')
    
    def test_products_in_the_cart_are_displayed_in_the_shop(self):
        '''Тест: продукты, добавленные в корзину, отображаются в магазине'''
        user = User.objects.create(
            username='Bill',
            email='bill@example.com'
        )
        product = Product.objects.create(
            name="Сумка 1",
            price=1250,
            image=self.image
        )
        Cart.objects.create(
            product=product,
            user=user
        )
        response = self.client.get(reverse('shop'))
        self.assertContains(response, 'Сумка 1')
