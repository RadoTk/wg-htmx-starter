from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['address', 'postal_code', 'country', 'phone_number']

class CombinedUserProfileForm(forms.Form):
    user_form: UserForm
    profile_form: UserProfileForm

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        
        self.user_form = UserForm(instance=user, prefix='user', data=kwargs.get('data') if kwargs.get('data') else None)
        self.profile_form = UserProfileForm(instance=user.profile, prefix='profile', data=kwargs.get('data') if kwargs.get('data') else None)

    def is_valid(self):
        return self.user_form.is_valid() and self.profile_form.is_valid()

    def save(self):
        self.user_form.save()
        self.profile_form.save()
