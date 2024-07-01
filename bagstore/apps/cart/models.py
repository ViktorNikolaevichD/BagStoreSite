from django.contrib.auth import get_user_model
from django.db import models

from apps.shop.models import Product


User = get_user_model()


class Cart(models.Model):
    '''Корзина покупок'''
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар в корзине')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь корзины')
