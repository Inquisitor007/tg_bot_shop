import asyncio

from aiogram import Bot
from aiogram.types import ChatMemberLeft
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from apps.tgbot.models import SubscribeChat


async def check_subscribes(bot: Bot, user_id: int, groups: list[SubscribeChat]):
    result = await asyncio.gather(*[
        asyncio.create_task(bot.get_chat_member(chat_id=group.chat_id, user_id=user_id))
        for group in groups]
    )

    if any(isinstance(user, ChatMemberLeft) for user in result):
        return False
    return True


async def subscribes_keyboard_factory(groups: list[SubscribeChat]):
    buttons: list[list[InlineKeyboardButton]] = []

    for group in groups:
        buttons.append([InlineKeyboardButton(text=group.name, callback_data=f'{group.id}', url=group.url)])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

