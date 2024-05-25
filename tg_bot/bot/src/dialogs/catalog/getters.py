from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.common import ManagedScroll

from asgiref.sync import sync_to_async

from apps.tgbot.models import User
from apps.catalog.models import Category, Product
from apps.cart.models import Cart, CartItem
from project.settings import MEDIA_ROOT


async def main_categories_getter(dialog_manager: DialogManager,
                                 event_from_user: User,
                                 **kwargs):
    raw_categories = await sync_to_async(list)(Category.objects.filter(category__isnull=True))
    categories = [(category.name, category.pk) for category in raw_categories]
    return {'categories': categories,
            'pages': len(categories) / 5 > 1}


async def subcategory_getter(dialog_manager: DialogManager,
                             event_from_user: User,
                             **kwargs):
    if not dialog_manager.dialog_data.get("category_id"):
        category_id = dialog_manager.event.data.split(':')[1]
        dialog_manager.dialog_data['category_id'] = category_id
    else:
        category_id = dialog_manager.dialog_data.get("category_id")

    raw_subcategories = await sync_to_async(list)(Category.objects.filter(category_id=category_id))
    subcategories = [(subcategory.name, subcategory.pk) for subcategory in raw_subcategories]
    return {'subcategories': subcategories,
            'pages': len(subcategories) / 5 > 1}


async def products_getter(dialog_manager: DialogManager, user: User, **kwargs):
    scroll: ManagedScroll = dialog_manager.find('pages')
    media_number = await scroll.get_page()

    products = dialog_manager.dialog_data.get("products", [])
    if not products:
        subcategory_id = dialog_manager.event.data.split(':')[1]
        raw_products = await sync_to_async(list)(Product.objects.filter(subcategory_id=subcategory_id))
        dialog_manager.dialog_data["products"] = raw_products
        products = dialog_manager.dialog_data.get("products", [])
    current_product = products[media_number]
    product_item = await get_product_item(current_product, user)
    dialog_manager.dialog_data['current_product'] = current_product
    dialog_manager.dialog_data['current_cart_product_item'] = product_item

    media = MediaAttachment(
        path=MEDIA_ROOT[:-6] + current_product.imagine.url,
        type=ContentType.PHOTO,
    )

    return {
        "media_count": len(products),
        "media_number": media_number + 1,
        "media": media,
        "description": current_product.description,
        'products_count': 0 if not product_item else product_item.quantity,
        'pages': len(products) > 1
    }


async def get_product_item(product: Product, user: User) -> CartItem:
    cart: Cart = await sync_to_async(Cart.objects.get)(user=user)
    item_exists: bool = await sync_to_async(CartItem.objects.filter(cart=cart, product=product).exists)()
    if not item_exists:
        return False
    return await sync_to_async(CartItem.objects.get)(cart=cart, product=product)
