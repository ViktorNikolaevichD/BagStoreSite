import os
import time

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from apps.cart.models import Cart
from apps.shop.models import Product

User = get_user_model()

class CartModelTest(TestCase):
    '''Тест модели корзины'''

    def setUp(self):
        '''Установка перед тестированием'''
        self.image = SimpleUploadedFile(
            name='test_image.jpg',
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
    
    def test_cart_is_related_to_cart(self):
        '''Тест: связь продукта с корзиной'''
        product = Product.objects.create(
            name='Сумка первая',
            price=1590,
            image=self.image
        )

        cart = Cart.objects.create(
            product=product,
            user=self.user
        )

        self.assertIn(cart, product.cart_set.all())
    def test_cart_cannot_be_without_the_user_and_the_product(self):
        '''Тест: корзина не может быть без пользователя и продукта'''
        cart = Cart()

        with self.assertRaises(ValidationError):
            cart.full_clean()
            cart.save()

    def test_another_user_does_not_see_someone_else_cart(self):
        '''Тест: другой пользователь не видит чужой корзины'''
        user = User.objects.create(
            username='Edith',
            email='edith@example.com'
        )
        product = Product.objects.create(
            name='Сумка первая',
            price=1590,
            image=self.image
        )

        Cart.objects.create(
            product=product,
            user=self.user
        )
        second_user_cart = Cart.objects.create(
            product=product,
            user=user
        )

        first_user_products = Cart.objects.filter(user=self.user)
        self.assertNotIn(second_user_cart, first_user_products)
    
    def test_saving_and_retrieving_carts(self):
        '''Тест: можно добавить товары в корзину и они там будут'''
        first_product = Product.objects.create(
            name='Сумка первая',
            price=1590,
            image=self.image
        )
        second_product = Product.objects.create(
            name='Сумка вторая',
            price=2090,
            image=self.image
        )
        Cart.objects.create(
            product=first_product,
            user=self.user
        )
        Cart.objects.create(
            product=second_product,
            user=self.user
        )
    
        carts = Cart.objects.all()
        self.assertEqual(carts.count(), 2)
    
    def test_can_add_the_same_items_to_the_cart(self):
        '''Тест: можно добавить одинаковые товары в корзину'''
        product = Product.objects.create(
            name='Сумка первая',
            price=1590,
            image=self.image
        )

        Cart.objects.create(
            product=product,
            user=self.user
        )
        Cart.objects.create(
            product=product,
            user=self.user
        )
        
        carts = Cart.objects.all()
        self.assertEqual(carts.count(), 2)