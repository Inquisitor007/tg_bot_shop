from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import Context
from asgiref.sync import sync_to_async

from apps.tgbot.models import User
from apps.cart.models import CartItem

from .services import get_total_price


async def cart_products_getter(dialog_manager: DialogManager, user: User, **kwargs):
    raw_cart_items = await sync_to_async(list)(CartItem.objects.filter(cart__user=user))
    if not raw_cart_items:
        return {
            'cart_title': 'Ваша корзина пуста',
            'cart_products': [],
            'pages': False,
        }
    cart_items = [(f'{await sync_to_async(str)(item)} - {item.quantity} - {item.item_total_price()}', item.id)
                  for item in raw_cart_items]
    total_price = get_total_price(raw_cart_items)
    return {'cart_products': cart_items,
            'cart_title': f'Ваша корзина на сумму: {total_price}руб.',
            'pages': len(cart_items) / 10 > 1,
            'is_products': len(cart_items) > 0}


async def order_data_getter(dialog_manager: DialogManager, aiogd_context: Context, user: User, **kwargs):
    dialog_data = aiogd_context.widget_data
    return {'check_order_data': f'Адрес доставки: {dialog_data["address"]}\nФИО: {dialog_data["fio"]}'}
