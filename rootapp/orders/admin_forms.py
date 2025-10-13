# from django import forms
# from .models import Order, OrderStatus

# class OrderAdminForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ["status"]

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         print("✅ OrderAdminForm loaded")

#         instance = kwargs.get("instance")
#         if instance and instance.pk:
#             allowed_codes = instance.get_allowed_status_transitions()
#             self.fields["status"].queryset = OrderStatus.objects.filter(code__in=allowed_codes)
#         else:
#             self.fields["status"].queryset = OrderStatus.objects.filter(is_active=True)
