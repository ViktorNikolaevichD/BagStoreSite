import os
import time

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.shop.models import Product


class ItemModelTest(TestCase):
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

    def test_saving_and_retrieving_items(self):
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
