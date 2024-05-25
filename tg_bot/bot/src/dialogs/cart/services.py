from apps.cart.models import CartItem


def get_total_price(cart_items: list[CartItem]):
    return sum(item.item_total_price() for item in cart_items)