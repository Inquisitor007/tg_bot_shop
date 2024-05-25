from asgiref.sync import async_to_sync, sync_to_async
from celery import shared_task
from aiogram import Bot
import environs

from django.conf import settings

from apps.tgbot.models import User


env = environs.Env()
env.read_env()


async def mailing(user_id, text):
    bot = Bot(token=env('BOT_TOKEN'))
    await bot.send_message(chat_id=user_id, text=text)



@shared_task
def add(user_id, text):
    return async_to_sync(mailing)(user_id, text)
