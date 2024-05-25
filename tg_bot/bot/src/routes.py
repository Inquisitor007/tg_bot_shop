from .handlers import commands_router, payment_router, inline_mode_router
from .dialogs import get_dialog_routes


def get_routers():
    return [commands_router, inline_mode_router, payment_router, *get_dialog_routes()]
