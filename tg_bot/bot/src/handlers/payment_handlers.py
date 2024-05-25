import asyncio

from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.types import PreCheckoutQuery, Message
from aiogram_dialog import DialogManager, StartMode

from asgiref.sync import sync_to_async

from tg_bot.bot.src.states import MainMenuSG
from tg_bot.bot.src.utils.order_writer import CSVWriter

payment_router = Router()


@payment_router.pre_checkout_query(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@payment_router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: Message, writer: CSVWriter, dialog_manager: DialogManager):
    order = dialog_manager.dialog_data.get('order')
    order.paid = True
    await message.answer(text='Платеж прошел успешно.\nСпасибо за покупку!')
    await dialog_manager.start(state=MainMenuSG.menu, mode=StartMode.RESET_STACK)
    await sync_to_async(order.save)()
    await asyncio.to_thread(writer.writerow, ([order.pk, order.user, order.address, order.fio, order.total_price]))




