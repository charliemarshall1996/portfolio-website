from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, UpdateView, DetailView, CreateView

from .models import Company, Contact, Interaction


def dashboard_view(request):
    return render(request, "crm/dashboard.html")


class CompanyListView(ListView, LoginRequiredMixin):
    model = Company
    paginate_by = 10
    ordering = ["-name"]


class CompanyDetailView(DetailView, LoginRequiredMixin):
    model = Company

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contacts"] = Contact.objects.filter(company=self.object.pk)
        return context


class CompanyCreateView(CreateView, LoginRequiredMixin):
    model = Company
    fields = [
        "name",
        "industry",
        "website",
        "linkedin",
        "phone",
        "email",
        "city",
        "region",
        "country",
        "status",
        "notes",
    ]
    success_url = reverse_lazy("company-list")


class CompanyUpdateView(UpdateView, LoginRequiredMixin):
    model = Company
    fields = [
        "name",
        "industry",
        "website",
        "linkedin",
        "phone",
        "email",
        "city",
        "region",
        "country",
        "status",
        "notes",
    ]

    def get_success_url(self):
        # Redirect to the detail view of the updated company
        return reverse("company-detail", kwargs={"pk": self.object.pk})


class ContactListView(ListView, LoginRequiredMixin):
    model = Contact
    paginate_by = 10
    ordering = ["-company__name"]


class ContactDetailView(DetailView, LoginRequiredMixin):
    model = Contact

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["interactions"] = Interaction.objects.filter(
            contact=self.object)
        return context


class ContactCreateView(CreateView, LoginRequiredMixin):
    model = Contact
    fields = [
        "first_name",
        "last_name",
        "job_title",
        "company",
        "email",
        "phone",
        "linkedin",
        "is_primary",
        "notes",
    ]
    success_url = reverse_lazy("contact-list")


class ContactUpdateView(UpdateView, LoginRequiredMixin):
    model = Contact
    fields = [
        "first_name",
        "last_name",
        "job_title",
        "company",
        "email",
        "phone",
        "linkedin",
        "is_primary",
        "notes",
    ]

    def get_success_url(self):
        # Redirect to the detail view of the updated company
        return reverse("contact-detail", kwargs={"pk": self.object.pk})


# Interaction


class InteractionListView(ListView, LoginRequiredMixin):
    model = Interaction
    paginate_by = 10
    ordering = ["-company__name"]


class InteractionDetailView(DetailView, LoginRequiredMixin):
    model = Interaction


class InteractionCreateView(CreateView, LoginRequiredMixin):
    model = Interaction
    fields = [
        "company",
        "contact",
        "medium",
        "summary",
        "detail",
        "date",
        "time",
        "follow_up",
    ]
    success_url = reverse_lazy("interaction-list")


class InteractionUpdateView(UpdateView, LoginRequiredMixin):
    model = Contact
    fields = [
        "company",
        "contact",
        "medium",
        "summary",
        "detail",
        "date",
        "time",
        "follow_up",
    ]

    def get_success_url(self):
        # Redirect to the detail view of the updated company
        return reverse("interaction-detail", kwargs={"pk": self.object.pk})
