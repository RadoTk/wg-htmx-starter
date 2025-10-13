from wagtail.admin.viewsets.model import ModelViewSet
from wagtail import hooks
from .models import Order

class OrderViewSet(ModelViewSet):
    model = Order
    menu_label = "Commandes"
    menu_icon = "doc-full"  # Icône pour le menu
    menu_order = 200
    add_to_admin_menu = True

    add_view_enabled = False
    edit_view_enabled = True
   
    form_fields = ["status"]

    inspect_view_enabled = True
    inspect_view_fields = [
        "formatted_items_table",
    ]

    list_display = [
        "id", 
        "colored_status",  
        "shopper_full_name", 
        "shopper_email", 
        "shopper_country", 
        "created_at", 
        "view_items_link"
    ]
    
    list_filter = ["status"]
    search_fields = ["shopper_name", "shopper_email", "shopper_first_name"]
    
    icon = "doc-full" 
    header_icon = "doc-full"

@hooks.register("register_admin_viewset")
def register_order_viewset():
    return OrderViewSet()