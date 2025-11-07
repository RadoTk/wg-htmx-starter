from django.shortcuts import render, get_object_or_404
from wagtail.models import Page

def load_slider(request, page_id):
    page = get_object_or_404(Page, id=page_id).specific
    slides = []

    if hasattr(page, "slider") and page.slider:
        slides = [
            item.slide for item in page.slider.slide_items.select_related("slide__background_image", "slide__right_image")
        ]

    return render(request, "partials/slider.html", {"slides": slides})
