import os
import time

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.shop.models import Product, Cart


User = get_user_model()


class ProductModelTest(TestCase):
    '''Тест модели товара'''

    def setUp(self):
        '''Установка перед тестированием'''
        
        self.first_image = SimpleUploadedFile(
            name='test_first_image.jpg',
            content=open(
                'apps/shop/tests/media_for_tests/woman.png', 'rb').read(),
            content_type='image/jpeg'
        )
        self.second_image = SimpleUploadedFile(
            name='test_second_image.jpg',
            content=open(
                'apps/shop/tests/media_for_tests/woman.png', 'rb').read(),
            content_type='image/jpeg'
        )

    def tearDown(self):
        '''Удаление параметров тестирования'''
        for product in Product.objects.all():
            if product is not None:
                os.remove(product.image.path)

    def test_saving_and_retrieving_products(self):
        '''Тест: можно сохранять и получать продукцию'''
        first_product = Product()
        first_product.name = 'Сумка первая'
        first_product.price = 1590
        first_product.image = self.first_image
        first_product.save()

        second_product = Product()
        second_product.name = 'Сумка вторая'
        second_product.price = 2999
        second_product.image = self.second_image
        second_product.save()

        saved_items = Product.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_product = saved_items[0]
        second_saved_product = saved_items[1]

        self.assertEqual(first_saved_product.name, 'Сумка первая')
        self.assertEqual(first_saved_product.price, 1590)
        self.assertRegex(first_saved_product.image.path,
                         r'shop[\\/]product_photo[\\/]')

        self.assertEqual(second_saved_product.name, 'Сумка вторая')
        self.assertEqual(second_saved_product.price, 2999)
        self.assertRegex(second_saved_product.image.path,
                         r'shop[\\/]product_photo[\\/]')

    def test_cannot_save_empty_products(self):
        '''Тест: нельзя добавлять пустые элементы продукции'''
        product = Product()
        with self.assertRaises(ValidationError):
            product.full_clean()
            product.save()

    def test_duplicate_products_are_valid(self):
        '''Тест: повторные элементы продукции допустимы'''
        Product.objects.create(
            name='Сумка первая',
            price=1590,
            image=self.first_image
        )
        product = Product(
            name='Сумка вторая',
            price=2999,
            image=self.second_image
        )
        product.full_clean()  # Не должно вызвать исключение

    def test_string_representation(self):
        '''Тест строкового представления'''
        product = Product(
            name='Сумка первая',
            price=1590,
            image=self.first_image
        )
        self.assertEqual(str(product), 'Сумка первая')


class CartModelTest(TestCase):
    '''Тест модели корзины'''

    def setUp(self):
        '''Установка перед тестированием'''
        self.image = SimpleUploadedFile(
            name='test_image.jpg',
            content=open(
                'apps/shop/tests/media_for_tests/woman.png', 'rb').read(),
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
        product = Product.objects.create(
            name='Сумка первая',
            price=1590,
            image=self.image
        )
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


class EvaluationModelTest(TestCase):
    '''Тест модели оценки продукта'''

    def setUp(self):
        '''Установка перед тестированием'''
        self.image = SimpleUploadedFile(
            name='test_image.jpg',
            content=open(
                'apps/shop/tests/media_for_tests/woman.png', 'rb').read(),
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
