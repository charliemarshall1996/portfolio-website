from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import (ListView,
                                  UpdateView,
                                  DeleteView,
                                  DetailView,
                                  CreateView)

from .forms import CompanyForm
from .models import Company, Contact, Interaction
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


class ContactListView(ListView):
    model = Contact
    paginate_by = 10
    ordering = ["-company__name"]


class ContactDetailView(DetailView):
    model = Contact

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['interactions'] = Interaction.objects.filter(
            contact=self.object)
        return context


class ContactCreateView(CreateView):
    model = Contact
    fields = [
        'first_name',
        'last_name',
        'job_title',
        'company',
        'email',
        'phone',
        'linkedin',
        'is_primary',
        'notes'
    ]
    success_url = reverse_lazy('crm:contacts')


class ContactUpdateView(UpdateView):
    model = Contact
    fields = [
        'first_name',
        'last_name',
        'job_title',
        'company',
        'email',
        'phone',
        'linkedin',
        'is_primary',
        'notes'
    ]

    def get_success_url(self):
        # Redirect to the detail view of the updated company
        return reverse('crm:contact', kwargs={'pk': self.object.pk})
