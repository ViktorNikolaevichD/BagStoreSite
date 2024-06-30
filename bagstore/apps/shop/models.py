from django.db import models


class Product(models.Model):
    '''Продукция в магазине'''
    name = models.CharField(max_length=100, verbose_name='Название')
    price = models.IntegerField(verbose_name='Цена')
    image = models.ImageField(upload_to='shop/product_photo/%Y/%m/%d/', 
                              verbose_name='Изображение')

    def __str__(self):
        '''Строковое представление'''
        return "%s" % str(self.name)
