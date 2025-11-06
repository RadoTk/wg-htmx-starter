from django.urls import path
from . import views
app_name = "base"
urlpatterns = [
    path("load-slider/", views.load_slider, name="load_slider"),
]
