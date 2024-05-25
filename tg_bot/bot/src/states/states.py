from aiogram.fsm.state import State, StatesGroup


class MainMenuSG(StatesGroup):
    menu = State()


class CatalogSG(StatesGroup):
    main_categories = State()
    subcategory = State()
    products = State()


class CartSG(StatesGroup):
    cart = State()
    address = State()
    fio = State()
    do_order = State()
