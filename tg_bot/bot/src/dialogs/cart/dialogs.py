from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import ListGroup, ScrollingGroup, Button, Row, Start, Next, Back
from aiogram_dialog.widgets.text import Format, Const

from .getters import cart_products_getter, order_data_getter
from .handlers import delete_item_from_cart, message_on_success, message_on_error, content_type_message_error, \
    order_invoice
from .filters import address_type_factory, fio_type_factory
from tg_bot.bot.src.getters.kbd import get_scroll_buttons
from tg_bot.bot.src.states import CartSG, MainMenuSG, CatalogSG

cart_dialog = Dialog(
    Window(
        Format('{cart_title}'),
        ScrollingGroup(
            ListGroup(Button(text=Format('❌      {item[0]}'), id='cart_product', on_click=delete_item_from_cart),
                      items='cart_products',
                      id='cart_product_list',
                      item_id_getter=lambda x: x[1]),
            id='cart_products',
            width=1,
            height=10,
            hide_pager=True
        ),
        get_scroll_buttons('cart_products'),
        Next(text=Format('Перейти к заполнению данных'), id='do_order', when='is_products'),
        Start(text=Format('Перейти в каталог'), id='to_catalog', state=CatalogSG.main_categories),
        Start(text=Format('Перейти в главное меню'), id='to_catalog', state=MainMenuSG.menu),
        state=CartSG.cart,
        getter=cart_products_getter
    ),
    Window(
        Format(text="""Введите адрес доставки в формате:\n'Страна, Регион, Город, Улица, Дом, Квартира'\n\nНапример:\n'Россия, Московская область, Москва, Пушкина, 12, 12'"""),
        TextInput(
            type_factory=address_type_factory,
            on_success=message_on_success,
            on_error=message_on_error,
            id='address'
        ),
        MessageInput(
            func=content_type_message_error,
            content_types=ContentType.ANY,
        ),
        Back(text=Format('Назад'), id='back'),
        Start(text=Format('Перейти в главное меню'), id='to_menu', state=MainMenuSG.menu),
        state=CartSG.address
    ),
    Window(
        Format(text='Отправьте ФИО получателя'),
        TextInput(
            type_factory=fio_type_factory,
            on_success=message_on_success,
            on_error=message_on_error,
            id='fio'
        ),
        MessageInput(
            func=content_type_message_error,
            content_types=ContentType.ANY,
        ),
        Back(text=Format('Назад'), id='back'),
        Start(text=Format('Перейти в главное меню'), id='to_menu', state=MainMenuSG.menu),
        state=CartSG.fio,
    ),
    Window(
        Format(text='{check_order_data}'),
        Button(text=Format('Оплатить заказ'), id='do_order', on_click=order_invoice),
        Back(text=Format('Назад'), id='back'),
        Start(text=Format('Перейти в главное меню'), id='to_menu', state=MainMenuSG.menu),
        state=CartSG.do_order,
        getter=order_data_getter
    ),
    # Window(
    #     Format(text='Ваш заказ оформлен'),
    #     Back(text=Format('Назад'), id='back'),
    #     Start(text=Format('Перейти в главное меню'), id='to_catalog', state=MainMenuSG.menu),
    #     state=CartSG.do_order,
    # )
)
