
from . import models

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

# Create your views here.


def home_view(request):
    context = {
        "qualifications": models.Qualification.objects.all().order_by("ongoing", "-date_earned"),
        "skills": models.Skill.objects.all().order_by("name"),
    }
    return render(request, "core/home.html", context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('freesites:queue_list')  # Redirect after login
        else:
            return render(request, 'core/login.html', {'error': 'Invalid credentials'})

    return render(request, 'core/login.html')
