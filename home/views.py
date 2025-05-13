from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render


# Create your views here.


def home_view(request, *args, **kwargs):
    return render(request, "home/home.html", {})


def services_view(request, *args, **kwargs):
    return render(request, "home/services.html", {})


@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'detail': 'CSRF cookie set'})
