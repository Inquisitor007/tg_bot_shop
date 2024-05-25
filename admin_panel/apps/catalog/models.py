from django.db import models


class Category(models.Model):
    category = models.ForeignKey('self', related_name='subcategories',
                                 on_delete=models.CASCADE, blank=True,
                                 null=True,
                                 limit_choices_to={'category__isnull': True})
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class AvailableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(available=True)


class Product(models.Model):
    subcategory = models.ForeignKey(Category, related_name='products',
                                    on_delete=models.CASCADE,
                                    limit_choices_to={
                                        'category__isnull': False})
    imagine = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    objects = AvailableManager()

    def __str__(self):
        return f'{self.subcategory.name} - {self.description[:20]}'

    class Meta:
        ordering = ['subcategory', 'name']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
