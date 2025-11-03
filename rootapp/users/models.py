from django.db import models
from django.contrib.auth.models import User
from rootapp.orders.models import Country 

from django.db.models.signals import post_save
from django.dispatch import receiver

from wagtail.models import Page
 
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from wagtail.admin.panels import FieldPanel
 

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    address = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=16, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)  

    def __str__(self):
        return f"Profil de {self.user.username}"



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
class SignupPage(Page):
    intro = models.TextField(help_text="Introductory text for the signup page")

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def serve(self, request):
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save()
                # Redirige après une inscription réussie
                return redirect('users:login')
        else:
            form = SignupForm()

        return render(request, 'users/signup_page.html', {'page': self, 'form': form})

