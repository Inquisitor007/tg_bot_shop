from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from asgiref.sync import sync_to_async

from apps.tgbot.models import SubscribeChat
from tg_bot.bot.src.utils.subscribes import check_subscribes, subscribes_keyboard_factory


class SubscribeMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any]
    ) -> Any:
        user = data.get('event_from_user')
        is_subscribe = True
        if user:
            groups = await sync_to_async(list)(SubscribeChat.objects.all())
            is_subscribe = await check_subscribes(bot=event.bot, user_id=user.id, groups=groups)
        if not is_subscribe:
            markup = await subscribes_keyboard_factory(groups=groups)
            await event.message.answer(text='Для использования бота подпишитесь на группы:',
                                       reply_markup=markup)
            return
        return await handler(event, data)
