from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import ManagedScroll
from aiogram_dialog.widgets.kbd import Button

from asgiref.sync import sync_to_async
from django.db.models import F

from apps.tgbot.models import User
from apps.catalog.models import Product
from apps.cart.models import Cart, CartItem


async def category_id_clear(_, __, dialog_manager: DialogManager, **kwargs):
    if dialog_manager.dialog_data.get("category_id"):
        dialog_manager.dialog_data["category_id"] = None


async def products_clear(_, __, dialog_manager: DialogManager, **kwargs):
    if dialog_manager.dialog_data.get("products"):
        dialog_manager.dialog_data["products"] = None
    scroll: ManagedScroll = dialog_manager.find('pages')
    await scroll.set_page(0)


async def change_cart(_, widget: Button, dialog_manager: DialogManager, **kwargs):
    button_id = widget.widget_id
    if button_id == 'add':
        await add_to_cart(dialog_manager)
    else:
        await delete_from_cart(dialog_manager)


async def add_to_cart(dialog_manager: DialogManager):
    cart_product_item: CartItem = dialog_manager.dialog_data['current_cart_product_item']
    if not cart_product_item:
        product = dialog_manager.dialog_data.get('current_product')
        user = dialog_manager.middleware_data.get('user')
        cart: Cart = await sync_to_async(Cart.objects.get)(user=user)
        await sync_to_async(CartItem.objects.create)(cart=cart, product=product)
        return
    cart_product_item.quantity = F('quantity') + 1
    await sync_to_async(cart_product_item.save)()


async def delete_from_cart(dialog_manager: DialogManager):
    cart_product_item: CartItem = dialog_manager.dialog_data['current_cart_product_item']
    if not cart_product_item:
        return
    if cart_product_item.quantity == 1:
        await sync_to_async(cart_product_item.delete)()
        return
    cart_product_item.quantity = F('quantity') - 1
    await sync_to_async(cart_product_item.save)()
