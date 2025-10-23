from django.urls import path
from . import views
from .views import UserLoginView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]
