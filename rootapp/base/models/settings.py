from django.conf import settings
from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import (
    BaseGenericSetting, BaseSiteSetting, register_setting
)
from wagtail.models import PreviewableMixin, Task, TaskState
from modelcluster.models import ClusterableModel
from django.utils.translation import gettext as _


@register_setting(icon="cog")
class GenericSettings(ClusterableModel, PreviewableMixin, BaseGenericSetting):
    mastodon_url = models.URLField(verbose_name="Mastodon URL", blank=True)
    github_url = models.URLField(verbose_name="GitHub URL", blank=True)
    organisation_url = models.URLField(verbose_name="Organisation URL", blank=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("github_url"),
                FieldPanel("mastodon_url"),
                FieldPanel("organisation_url"),
            ],
            "Social settings",
        )
    ]

    def get_preview_template(self, request, mode_name):
        return "base.html"


@register_setting(icon="site")
class SiteSettings(BaseSiteSetting):
    title_suffix = models.CharField(
        verbose_name="Title suffix",
        max_length=255,
        default="The Wagtail Bakery",
    )
    panels = [FieldPanel("title_suffix")]


class UserApprovalTaskState(TaskState):
    pass


class UserApprovalTask(Task):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=False
    )

    admin_form_fields = Task.admin_form_fields + ["user"]
    task_state_class = UserApprovalTaskState
    admin_form_readonly_on_edit_fields = Task.admin_form_readonly_on_edit_fields + [
        "user"
    ]

    def user_can_access_editor(self, page, user):
        return user == self.user

    def page_locked_for_user(self, page, user):
        return user != self.user

    def get_actions(self, page, user):
        if user == self.user:
            return [
                ("approve", "Approve", False),
                ("reject", "Reject", False),
                ("cancel", "Cancel", False),
            ]
        return []

    def on_action(self, task_state, user, action_name, **kwargs):
        if action_name == "cancel":
            return task_state.workflow_state.cancel(user=user)
        return super().on_action(task_state, user, action_name, **kwargs)

    def get_task_states_user_can_moderate(self, user, **kwargs):
        if user == self.user:
            return TaskState.objects.filter(
                status=TaskState.STATUS_IN_PROGRESS, task=self.task_ptr
            )
        return TaskState.objects.none()

    @classmethod
    def get_description(cls):
        return _("Only a specific user can approve this task")
