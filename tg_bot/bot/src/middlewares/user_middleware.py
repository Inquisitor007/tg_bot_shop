from typing import Callable, Any, Awaitable
from asgiref.sync import sync_to_async

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from apps.tgbot.models import User
from apps.cart.models import Cart


class UserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any]
    ) -> Any:
        user = data.get('event_from_user')
        if user and not data.get('user'):
            user, is_created = await sync_to_async(User.objects.get_or_create)(user_id=str(user.id))
            if is_created:
                await sync_to_async(Cart.objects.create)(user=user)
            data['user'] = user
        return await handler(event, data)