from django.shortcuts import render
from . import models

# Create your views here.


def home_view(request):
    context = {
        "qualifications": models.Qualification.objects.all(),
        "skills": models.Skill.objects.all(),
    }
    return render(request, "core/home.html", context)
