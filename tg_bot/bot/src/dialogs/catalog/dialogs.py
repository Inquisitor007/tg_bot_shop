from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Column, Cancel, ScrollingGroup, NumberedPager, NextPage, PrevPage, CurrentPage, \
    Row, FirstPage, LastPage, SwitchTo, ListGroup, Button, Back, StubScroll, Group, Start
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format, List, Const

from tg_bot.bot.src.states import MainMenuSG, CatalogSG, CartSG
from .getters import main_categories_getter, subcategory_getter, products_getter
from ...getters.kbd import get_scroll_buttons
from .handlers import category_id_clear, products_clear, change_cart

catalog_dialog = Dialog(
    Window(
        Format('Выберите категорию'),
        ScrollingGroup(
            ListGroup(SwitchTo(text=Format('{item[0]}'), id='category', state=CatalogSG.subcategory),
                      items='categories',
                      id='category_list',
                      item_id_getter=lambda x: x[1]),
            id='main_categories',
            width=2,
            height=2,
            hide_pager=True
        ),
        get_scroll_buttons('main_categories'),
        Cancel(text=Format('Вернуться в главное меню'),
               id='to_menu'),
        state=CatalogSG.main_categories,
        getter=main_categories_getter
    ),
    Window(
        Format('Выберите подкатегорию'),
        ScrollingGroup(
            ListGroup(SwitchTo(text=Format('{item[0]}'), id='subcategory', state=CatalogSG.products),
                      items='subcategories',
                      id='subcategory_list',
                      item_id_getter=lambda x: x[1]),
            id='subcategories',
            width=2,
            height=2,
            hide_pager=True
        ),
        get_scroll_buttons('subcategories'),
        Back(text=Format('Назад'), id='back', on_click=category_id_clear),
        Cancel(text=Format('Вернуться в главное меню'), id='to_menu'),
        state=CatalogSG.subcategory,
        getter=subcategory_getter
    ),
    Window(
        Format('{description}'),
        DynamicMedia(selector="media"),
        StubScroll(id="pages", pages="media_count"),
        get_scroll_buttons('pages'),
        Row(
            Button(Const(text='➖'), id='delete', on_click=change_cart),

            Button(text=Format('{products_count}'), id='add_to_cart'),

            Button(Const(text='➕'), id='add', on_click=change_cart),
        ),
        Back(text=Format('Назад'), id='back', on_click=products_clear),
        Start(text=Format('Перейти в корзину'), id='to_cart', state=CartSG.cart),
        Cancel(text=Format('Вернуться в главное меню'), id='to_menu'),
        state=CatalogSG.products,
        getter=products_getter
    )
)
