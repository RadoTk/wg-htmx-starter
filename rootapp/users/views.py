from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserForm, UserProfileForm

from django.contrib.auth import logout



from django.contrib.auth.views import LoginView

class UserLoginView(LoginView):
    template_name = 'users/login.html' 


@login_required
def profile_edit(request):
    user = request.user
    profile = user.profile 

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès.")
            return redirect('users:profile_edit')

        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'users/profile_edit.html', context)


def user_logout(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('users:login') 

