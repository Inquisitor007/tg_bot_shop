from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from tg_bot.bot.src.states import MainMenuSG

commands_router = Router()


@commands_router.message(CommandStart())
async def process_start(message: Message, dialog_manager: DialogManager, bot: Bot):
    await dialog_manager.start(state=MainMenuSG.menu, mode=StartMode.RESET_STACK)