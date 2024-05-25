from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.types import PreCheckoutQuery, Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from aiogram_dialog import DialogManager, StartMode

from tg_bot.bot.src.states import MainMenuSG

payment_router = Router()


@payment_router.pre_checkout_query(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@payment_router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: Message, dialog_manager: DialogManager):
    await message.answer(text='Платеж прошел успешно.\nСпасибо за покупку!')
    await dialog_manager.start(state=MainMenuSG.menu, mode=StartMode.RESET_STACK)



