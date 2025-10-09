from wagtail.admin.viewsets.model import ModelViewSet
from wagtail import hooks
from django.utils.html import format_html
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
        "formatted_items_table",
    ]

    list_display = ["id", "shopper_full_name", "shopper_email", "shopper_country", "created_at", "view_items_link"]
    search_fields = ["shopper_name", "shopper_email"]


@hooks.register("register_admin_viewset")
def register_order_viewset():
    return OrderViewSet()



#FIXE(AR): nouvelle "order" s'affiche mais "more options" ne s'execute pas, et le format  est différent a celle de wagtail
@hooks.register("insert_global_admin_js")
def add_htmx_script():
    return format_html(
        '<script src="https://unpkg.com/htmx.org@1.9.2"></script>'
    )

@hooks.register("insert_global_admin_js")
def auto_refresh_order_admin():
    return format_html("""
    <script>
      document.addEventListener('DOMContentLoaded', function () {{
        const path = window.location.pathname;
        const isIndex = path === '/admin/order/';

        if (!isIndex) return;

        const tbody = document.querySelector('table.listing tbody');
        if (!tbody) return;

        tbody.id = 'order-table-body';

        // ✅ Requête HTMX toutes les 10s
        setInterval(function () {{
          htmx.ajax('GET', '/orders/admin/orders/live/', '#order-table-body');
        }}, 10000);

        // ✅ Quand HTMX a terminé d'injecter le HTML
        document.body.addEventListener('htmx:afterSwap', function (evt) {{
          if (evt.target.id === 'order-table-body') {{
            // Relancer les scripts JS Wagtail (Stimulus)
            const event = new Event('wagtail:domready', {{ bubbles: true }});
            document.body.dispatchEvent(event);
          }}
        }});
      }});
    </script>
    """)

