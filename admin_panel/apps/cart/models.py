from django.db import models

from apps.catalog.models import Product
from apps.tgbot.models import User


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Cart for user:{self.user}'

    def total_price(self):
        return sum(item.item_total_price() for item in self.items.all())

    def clear(self):
        self.items.all().delete()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.name

    def item_total_price(self):
        return self.product.price * self.quantity
