from wagtail.admin.filters import WagtailFilterSet
from wagtail.admin.panels import FieldPanel
from wagtail.admin.viewsets.model import ModelViewSet
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from rootapp.base.filters import RevisionFilterSetMixin
from rootapp.breads.models import ProductIngredient, ProductCategory, ProductOrigin


# -----------------------------------------------------------------------------
# FILTERS
# -----------------------------------------------------------------------------

class ProductIngredientFilterSet(RevisionFilterSetMixin, WagtailFilterSet):
    class Meta:
        model = ProductIngredient
        fields = {
            "live": ["exact"],
        }


class ProductCategoryFilterSet(RevisionFilterSetMixin, WagtailFilterSet):
    class Meta:
        model = ProductCategory
        fields = []


# -----------------------------------------------------------------------------
# SNIPPET VIEWSETS
# -----------------------------------------------------------------------------

class ProductIngredientSnippetViewSet(SnippetViewSet):
    """
    Wagtail snippet admin view for ProductIngredient.
    """
    model = ProductIngredient
    ordering = ("name",)
    search_fields = ("name",)
    filterset_class = ProductIngredientFilterSet
    inspect_view_enabled = True


class ProductCategorySnippetViewSet(SnippetViewSet):
    """
    Wagtail snippet admin view for ProductCategory.
    """
    model = ProductCategory
    ordering = ("title",)
    search_fields = ("title",)
    filterset_class = ProductCategoryFilterSet
    inspect_view_enabled = True


class ProductOriginModelViewSet(ModelViewSet):
    """
    Wagtail model admin view for ProductOrigin.
    """
    model = ProductOrigin
    ordering = ("title",)
    search_fields = ("title",)
    icon = "globe"
    inspect_view_enabled = True

    panels = [
        FieldPanel("title"),
    ]


# -----------------------------------------------------------------------------
# SNIPPET GROUPING IN WAGTAIL ADMIN
# -----------------------------------------------------------------------------

class ProductDataGroup(SnippetViewSetGroup):
    """
    Group all product-related snippets in the Wagtail admin under one menu.
    """
    menu_label = "Product Data"
    menu_icon = "package"  # can be changed to "tag", "folder-open-inverse", etc.
    menu_order = 200  # controls order in sidebar

    items = (
        ProductIngredientSnippetViewSet,
        ProductCategorySnippetViewSet,
        ProductOriginModelViewSet,
    )


# Register the snippet group (registering individual snippets is not needed)
register_snippet(ProductDataGroup)
