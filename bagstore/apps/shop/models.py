from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


User = get_user_model()


class Product(models.Model):
    '''Продукция в магазине'''
    name = models.CharField(max_length=100, verbose_name='Название')
    price = models.IntegerField(verbose_name='Цена')
    image = models.ImageField(upload_to='shop/product_photo/%Y/%m/%d/', 
                              verbose_name='Изображение')

    def __str__(self):
        '''Строковое представление'''
        return "%s" % str(self.name)


class Evaluation(models.Model):
    '''Оценка товара'''
    evaluation = models.IntegerField(verbose_name='Оценка товара',
                                     validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                             verbose_name='Пользователь, поставивший оценку')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, 
                                verbose_name='Оцениваемый товар')
    
    class Meta:
        unique_together = ('user', 'product')
        