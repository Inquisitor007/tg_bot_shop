from django.contrib import admin

from apps.orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ['paid', 'created', 'update', 'total_price']
    search_fields = ['address', 'fio']