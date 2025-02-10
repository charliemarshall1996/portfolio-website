from django.shortcuts import render
from . import models

# Create your views here.


def home_view(request):
    context = {
        "qualifications": models.Qualification.objects.all().order_by("ongoing", "-date_earned"),
        "skills": models.Skill.objects.all().order_by("name"),
    }
    return render(request, "core/home.html", context)
