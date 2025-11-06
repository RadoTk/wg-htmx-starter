from django.shortcuts import render

def load_slider(request):
    # on ne passe aucune variable, juste afficher le HTML du slider
    return render(request, "partials/slider.html")
