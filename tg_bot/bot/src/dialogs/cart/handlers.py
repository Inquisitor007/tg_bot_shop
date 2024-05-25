from aiogram import Bot
from aiogram.types import Message, CallbackQuery, LabeledPrice
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, SwitchInlineQuery

import asyncio
from asgiref.sync import sync_to_async

from apps.tgbot.models import User
from apps.cart.models import CartItem
from apps.orders.models import Order, OrderItem


async def delete_item_from_cart(_, widget: Button, dialog_manager: DialogManager, **kwargs):
    item_id = dialog_manager.item_id
    await sync_to_async(CartItem.objects.filter(id=item_id).delete)()


async def message_on_success(message: Message,
                             widget: ManagedTextInput,
                             dialog_manager: DialogManager,
                             text: str):
    await dialog_manager.next()


async def message_on_error(message: Message,
                           widget: ManagedTextInput,
                           dialog_manager: DialogManager,
                           err: Exception | None = None):
    await message.answer(str(err))


async def content_type_message_error(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    await message.answer('Отправьте текстовое сообщение')


async def order_invoice(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, **kwargs):
    bot: Bot = dialog_manager.middleware_data.get('bot')
    user: User = dialog_manager.middleware_data.get('user')
    token = dialog_manager.middleware_data.get('payment_token')
    cart_items = await sync_to_async(list)(CartItem.objects.filter(cart__user=user))
    order = await create_order(dialog_manager, user, cart_items)
    prices = [
        LabeledPrice(label=f'{await sync_to_async(str)(item)}: {item.quantity}', amount=item.item_total_price() * 100)
        for item in cart_items
    ]
    await bot.send_invoice(chat_id=user.user_id,
                           title='Оплата заказа',
                           description=str(order),
                           provider_token=token,
                           currency='RUB',
                           prices=prices,
                           start_parameter='test',
                           payload='test-payload',
                           )
    user_cart = await sync_to_async(lambda: user.cart)()
    await sync_to_async(user_cart.clear)()


async def create_order(dialog_manager: DialogManager, user: User, items: list[CartItem]):
    dialog_data = dialog_manager.current_context().widget_data
    address = dialog_data.get('address')
    fio = dialog_data.get('fio')
    order = await sync_to_async(Order.objects.create)(user=user, address=address, fio=fio)
    await asyncio.gather(
        *[asyncio.create_task(
            sync_to_async(OrderItem.objects.create)(order=order,
                                                    product=await sync_to_async(lambda: item.product)(),
                                                    price=item.item_total_price(),
                                                    quantity=await sync_to_async(lambda: item.quantity)())
        )
            for item in items
        ]
    )
    return order
