from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Column, Start
from aiogram_dialog.widgets.text import Format

from tg_bot.bot.src.states import MainMenuSG, CartSG, CatalogSG

menu_dialog = Dialog(
    Window(
        Format('Главное меню'),
        Column(
            Start(text=Format('Каталог'),
                  id='to_catalog',
                  state=CatalogSG.main_categories),
            Start(text=Format('Корзина'),
                  id='to_cart',
                  state=CartSG.cart)

        ),
        state=MainMenuSG.menu,
    )
)