import os
import time

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from apps.shop.models import Product, Evaluation


User = get_user_model()


class ProductModelTest(TestCase):
    '''Тест модели товара'''

    def setUp(self):
        '''Установка перед тестированием'''
        
        self.first_image = SimpleUploadedFile(
            name='test_first_image.jpg',
            content=open(
                'bagstore/media_for_tests/woman.png', 'rb').read(),
            content_type='image/jpeg'
        )
        self.second_image = SimpleUploadedFile(
            name='test_second_image.jpg',
            content=open(
                'bagstore/media_for_tests/woman.png', 'rb').read(),
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

class EvaluationModelTest(TestCase):
    '''Тест модели оценки продукта'''

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

    def test_cant_rate_anonymously(self):
        '''Тест: нельзя поставить оценку анонимно'''
        product = Product.objects.create(
            name='Сумка первая',
            price=1590,
            image=self.image
        )
        evaluation = Evaluation(
            evaluation=2,
            product=product
        )
        with self.assertRaises(ValidationError):
            evaluation.full_clean()
            evaluation.save()

    def test_cant_rate_without_the_product(self):
        '''Тест: нельзя поставить оценку без продукта'''
        evaluation = Evaluation(
            evaluation=2,
            user=self.user
        )
        with self.assertRaises(ValidationError):
            evaluation.full_clean()
            evaluation.save()

    def test_cant_rate_the_same_product_twice(self):
        '''Тест: нельзя поставить оценку на один товар дважды'''
        product = Product.objects.create(
            name='Сумка первая',
            price=1590,
            image=self.image
        )
        Evaluation.objects.create(
            evaluation=2,
            product=product,
            user=self.user
        )
        
        evaluation = Evaluation(
            evaluation=5,
            product=product,
            user=self.user
        )
        with self.assertRaises(ValidationError):
            evaluation.full_clean()
            evaluation.save()
            

    def test_cant_put_a_evaluation_higher_than_five(self):
        '''Тест: нельзя поставить оценку выше пяти'''
        product = Product.objects.create(
            name='Сумка первая',
            price=1590,
            image=self.image
        )
        evaluation = Evaluation(
            evaluation=6,
            product=product,
            user=self.user
        )
        with self.assertRaises(ValidationError):
            evaluation.full_clean()
            evaluation.save()

    def test_cant_put_a_evaluation_less_than_one(self):
        '''Тест: нельзя поставить оценку ниже одного'''
        product = Product.objects.create(
            name='Сумка первая',
            price=1590,
            image=self.image
        )
        evaluation = Evaluation(
            evaluation=0,
            product=product,
            user=self.user
        )
        with self.assertRaises(ValidationError):
            evaluation.full_clean()
            evaluation.save()
