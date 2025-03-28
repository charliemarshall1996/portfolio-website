from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import (ListView,
                                  UpdateView,
                                  DeleteView,
                                  DetailView,
                                  CreateView)

from .forms import CompanyForm
from .models import Company, Contact
# Create your views here.


def home_view(request):
    return render(request, 'crm/home.html')


class CompanyListView(ListView):
    model = Company
    paginate_by = 10
    ordering = ["-name"]


class CompanyDetailView(DetailView):
    model = Company

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = Contact.objects.filter(company=self.object)
        return context


class CompanyCreateView(CreateView):
    model = Company
    fields = [
        'name',
        'industry',
        'website',
        'linkedin',
        'phone',
        'email',
        'city',
        'region',
        'country',
        'status',
        'notes'
    ]
    success_url = reverse_lazy('crm:companies')


class CompanyUpdateView(UpdateView):
    model = Company
    fields = [
        'name',
        'industry',
        'website',
        'linkedin',
        'phone',
        'email',
        'city',
        'region',
        'country',
        'status',
        'notes'
    ]

    def get_success_url(self):
        # Redirect to the detail view of the updated company
        return reverse('crm:company', kwargs={'pk': self.object.pk})
