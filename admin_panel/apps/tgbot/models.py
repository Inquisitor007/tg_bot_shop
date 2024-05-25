from django.db import models
from django.db.models import Manager

from apps.catalog.models import Product


class User(models.Model):
    user_id = models.CharField(max_length=15)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_id

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class SubscribeChat(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    chat_id = models.CharField(max_length=15)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы для подписки'


class FAQ(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Mailing(models.Model):
    users = models.ManyToManyField(User, related_name='mailings')
    message = models.TextField()

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return f'{self.message[:50]}'
