import os
import sys

import django

sys.path.append(os.getcwd() + '/admin_panel')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram_dialog import setup_dialogs
from aiogram.fsm.storage.redis import Redis, RedisStorage, DefaultKeyBuilder

import asyncio
import logging

from .bot.config import get_config
from .bot.src import get_routers, SubscribeMiddleware, UserMiddleware


async def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='[#{levelname} - {asctime}]\n{filename} - {name}|{funcName} - {lineno}: {message}\n',
                        style='{')

    config = get_config()
    redis = Redis(host=config.redis.host, port=config.redis.port)
    storage = RedisStorage(redis=redis, key_builder=DefaultKeyBuilder(with_destiny=True))
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher(storage=storage)
    dp.workflow_data.update({'payment_token': config.payment.token,})
    dp.include_routers(*get_routers())
    dp.update.middleware(SubscribeMiddleware())
    dp.update.middleware(UserMiddleware())
    # dp.startup.register(set_menu)
    setup_dialogs(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

#
if __name__ == '__main__':
    asyncio.run(main())
