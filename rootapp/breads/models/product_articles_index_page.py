from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .product_article_page import ProductArticlePage
from .model_mixins import PaginatedIndexMixin

class ProductArticlesIndexPage(Page, PaginatedIndexMixin):
    introduction = models.TextField(blank=True)
    image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("image"),
    ]

    subpage_types = ["ProductArticlePage"]
    api_fields = [APIField("introduction"), APIField("image")]

    def get_articles(self):
        return ProductArticlePage.objects.live().descendant_of(self).order_by("-first_published_at")

    def children(self):
        return self.get_children().specific().live()

    def paginate(self, request, articles, per_page=12):
        page_number = request.GET.get("page")
        paginator = Paginator(articles, per_page)
        try:
            pages = paginator.page(page_number)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    def get_context(self, request):
        context = super().get_context(request)
        articles = self.paginate(request, self.get_articles())
        context["articles"] = articles
        return context

    class Meta:
        verbose_name = "product articles index"
        verbose_name_plural = "product articles indexes"
