# models/settings.py

from wagtail.contrib.settings.models import BaseGenericSetting, BaseSiteSetting
from wagtail.admin.panels import FieldPanel

class GenericSettings(BaseGenericSetting):
    mastodon_url = models.URLField(verbose_name="Mastodon URL", blank=True)
    github_url = models.URLField(verbose_name="GitHub URL", blank=True)
    organisation_url = models.URLField(verbose_name="Organisation URL", blank=True)

    panels = [
        FieldPanel("github_url"),
        FieldPanel("mastodon_url"),
        FieldPanel("organisation_url"),
    ]

class SiteSettings(BaseSiteSetting):
    title_suffix = models.CharField(
        verbose_name="Title suffix",
        max_length=255,
        help_text="Suffix for the title meta tag.",
        default="The Wagtail Bakery",
    )

    panels = [
        FieldPanel("title_suffix"),
    ]
