from .main_menu import menu_dialog
from .catalog import catalog_dialog
from .cart import cart_dialog

def get_dialog_routes():
    return [menu_dialog, catalog_dialog, cart_dialog]

