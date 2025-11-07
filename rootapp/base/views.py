from django.shortcuts import get_object_or_404, render
from wagtail.models import Page
from .models import SliderPlacement

def load_slider(request, page_id, position):
    """Charge le slider associé à une page et une position (via htmx)."""
    page = get_object_or_404(Page, id=page_id)
    placement = (
        SliderPlacement.objects
        .select_related("slider")
        .filter(page=page, position=position)
        .first()
    )

    if not placement:
        return render(request, "partials/no_slider.html", {"position": position})

    # Tu peux personnaliser le template selon la position
    template_name = f"partials/slider_{position}.html"
    return render(request, template_name, {"slider": placement.slider})
