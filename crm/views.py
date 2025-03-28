from django.shortcuts import render
from django.views.generic import ListView, UpdateView, DeleteView, DetailView, CreateView

from .forms import CompanyForm
from .models import Company
# Create your views here.


def home_view(request):
    return render(request, 'crm/home.html')


class CompanyListView(ListView):
    model = Company
    paginate_by = 10
    ordering = ["-name"]
