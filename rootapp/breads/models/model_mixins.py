from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from wagtail.models import RevisionMixin

class WagtailPanelsAndAPIFieldsMixin:
    """Utility mixin for Wagtail FieldPanels and APIFields."""

    @classmethod
    def generate_panels(cls, fields):
        return [FieldPanel(f) for f in fields]

    @classmethod
    def generate_api_fields(cls, fields):
        return [APIField(f) for f in fields]


class WagtailRevisionMixin(RevisionMixin, models.Model):
    """Adds Wagtail revision support to a model."""

    revisions = GenericRelation(
        "wagtailcore.Revision",
        content_type_field="base_content_type",
        object_id_field="object_id",
        related_query_name=None,
        for_concrete_model=False,
    )

    class Meta:
        abstract = True


class PaginatedIndexMixin:
    """Provides pagination functionality for index pages."""

    def paginate_queryset(self, request, queryset, per_page=12):
        paginator = Paginator(queryset, per_page)
        page_number = request.GET.get("page")
        try:
            return paginator.page(page_number)
        except PageNotAnInteger:
            return paginator.page(1)
        except EmptyPage:
            return paginator.page(paginator.num_pages)
