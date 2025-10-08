from wagtail.admin.viewsets.model import ModelViewSet
from wagtail import hooks

from .models import Order


class OrderViewSet(ModelViewSet):
    model = Order
    menu_label = "Orders"
    menu_icon = "doc-full-inverse"
    menu_order = 200
    add_to_admin_menu = True

    add_view_enabled = False
    edit_view_enabled = False

    form_fields = []

    inspect_view_enabled = True
    inspect_view_fields = [
        "id",
        "shopper_full_name",
        "shopper_email",
        "shopper_address",
        "shopper_postal_code",
        "shopper_country",
        "created_at",
        "formatted_items_table",
        "get_total_items_cost",
    ]

    list_display = ["id", "shopper_full_name", "shopper_email", "shopper_country", "created_at"]
    search_fields = ["shopper_name", "shopper_email"]


@hooks.register("register_admin_viewset")
def register_order_viewset():
    return OrderViewSet()
