import os

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from apps.cart.models import Cart
from apps.shop.models import Product


User = get_user_model()


class CartPageTest(TestCase):
    '''Тест страницы корзины'''

    def setUp(self):
        '''Установка перед тестированием'''  
        self.image = SimpleUploadedFile(
            name='test_first_image.jpg',
            content=open(
                'bagstore/media_for_tests/woman.png', 'rb').read(),
            content_type='image/jpeg'
        )
        self.user = User.objects.create(
            username='Bill',
            email='bill@example.com'
        )
    
    def tearDown(self):
        '''Удаление параметров тестирования'''
        for product in Product.objects.all():
            if product is not None:
                os.remove(product.image.path)

    def test_cart_page_template(self):
        '''Тест: используется шаблон для страницы корзины'''
        response = self.client.get(reverse('cart'))
        
        self.assertTemplateUsed(response, 'cart.html')

    def test_all_the_users_products_are_passed_to_the_cart_template(self):
        '''Тест: в шаблон корзины передаются все продукты пользователя'''
        product1 = Product.objects.create(
            name="Сумка 1",
            price=1250,
            image=self.image
        )
        product2 = Product.objects.create(
            name="Сумка 2",
            price=1250,
            image=self.image
        )

        Cart.objects.create(
            product=product1,
            user=self.user
        )
        Cart.objects.create(
            product=product2,
            user=self.user
        )

        carts = Cart.objects.all()
        response = self.client.get(reverse('cart'))

        self.assertEqual(list(response.context['cart_list']), list(carts))

    def test_the_cart_template_displays_all_the_users_products(self):
        '''Тест: в шаблоне корзины отображаются все продукты пользователя'''
        product1 = Product.objects.create(
            name="Сумка 1",
            price=1250,
            image=self.image
        )
        product2 = Product.objects.create(
            name="Сумка 2",
            price=1250,
            image=self.image
        )

        Cart.objects.create(
            product=product1,
            user=self.user
        )
        Cart.objects.create(
            product=product2,
            user=self.user
        )

        response = self.client.get(reverse('cart'))

        self.assertContains(response, 'Сумка 1')
        self.assertContains(response, 'Сумка 2')

    def test_the_user_does_not_see_someone_else_cart(self):
        '''Тест: пользователь не видит чужой корзины'''
        self.fail('Доделать тест!')
        