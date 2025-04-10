from django.shortcuts import render


# Create your views here.


def home_view(request, *args, **kwargs):
    return render(request, "home/home.html", {})


def services_view(request, *args, **kwargs):
    return render(request, "home/services.html", {})
