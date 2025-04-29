from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, path
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import (
    SnippetViewSet, SnippetViewSetGroup, hooks)

from . import models


class CompanyViewSet(SnippetViewSet):
    model = models.Company
    menu_label = "Companies"
    icon = "office"
    list_display = ("name", "industry", "email", "phone")
    search_fields = ("name", "industry", "email")


class ContactViewSet(SnippetViewSet):
    model = models.Contact
    menu_label = "Contacts"
    icon = "user"
    list_display = ("first_name", "last_name", "company", "email", "phone")
    list_filter = ("company",)
    search_fields = ("first_name", "last_name", "email", "company__name")


class DealViewSet(SnippetViewSet):
    model = models.Deal
    menu_label = "Deals"
    icon = "list-ol"
    list_display = ("name", "company", "stage",
                    "amount", "expected_close_date")
    list_filter = ("stage", "company")
    search_fields = ("name", "company__name",
                     "contact__first_name", "contact__last_name")


class TaskViewSet(SnippetViewSet):
    model = models.Task
    menu_label = "Tasks"
    icon = "task"
    list_display = ("title", "related_to", "assigned_to",
                    "due_date", "priority", "status")
    list_filter = ("priority", "status", "related_to")
    search_fields = ("title", "related_to__name", "assigned_to__first_name")


class CRMViewSetGroup(SnippetViewSetGroup):
    menu_label = "CRM"
    menu_icon = "folder"
    menu_order = 200
    items = (CompanyViewSet, ContactViewSet, DealViewSet, TaskViewSet)


class ServiceTypeViewSet(SnippetViewSet):
    model = models.ServiceType
    menu_label = "Service Types"
    icon = "cog"
    list_display = ("name", "description")
    search_fields = ("name", "description")


class PricingOptionViewSet(SnippetViewSet):
    model = models.PricingOption
    menu_label = "Pricing Options"
    icon = "dollar"
    list_display = ("name", "service_type",
                    "pricing_model", "base_rate", "active")
    list_filter = ("service_type", "pricing_model", "active")
    search_fields = ("name", "service_type__name")


class ServiceViewSet(SnippetViewSet):
    model = models.Service
    menu_label = "Services"
    icon = "list-ul"
    list_display = ("name", "company", "service_type",
                    "status", "start_date", "target_date")
    list_filter = ("service_type", "status", "pricing_option")
    search_fields = ("name", "company__name",
                     "contact__first_name", "contact__last_name")
    list_export = [
        'name', 'company', 'contact', 'service_type', 'pricing_option',
        'status', 'start_date', 'target_date', 'completion_date'
    ]


class ServicesViewSetGroup(SnippetViewSetGroup):
    menu_label = "Services"
    menu_icon = "folder-open-inverse"
    menu_order = 210  # After CRM (200)
    items = (ServiceTypeViewSet, PricingOptionViewSet, ServiceViewSet)


class ContractTemplateViewSet(SnippetViewSet):
    model = models.ContractTemplate
    menu_label = "Contract Templates"
    icon = "doc-full"
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "description")


class InvoiceTemplateViewSet(SnippetViewSet):
    model = models.InvoiceTemplate
    menu_label = "Invoice Templates"
    icon = "doc-full"
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "description")


class ContractViewSet(SnippetViewSet):
    model = models.Contract
    menu_label = "Contracts"
    icon = "form"
    list_display = ("contract_id", "service", "company",
                    "status", "generated_date", "expiration_date")
    list_filter = ("status", "service__service_type", "template")
    search_fields = ("contract_id", "service__name", "company__name",
                     "contact__first_name", "contact__last_name")
    list_export = [
        'contract_id', 'service', 'company', 'contact', 'status',
        'generated_date', 'sent_date', 'approved_date', 'expiration_date'
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if qs:
            return qs.select_related('service', 'company', 'contact', 'template')
        else:
            return qs


class InvoiceViewSet(SnippetViewSet):
    model = models.Invoice
    menu_label = "Invoices"
    icon = "form"
    list_display = ("invoice_id", "service", "company",
                    "status", "issue_date", "due_date", "total")
    list_filter = ("status", "service__service_type", "template")
    search_fields = ("invoice_id", "service__name", "company__name",
                     "contact__first_name", "contact__last_name")
    list_export = [
        'invoice_id', 'service', 'company', 'contact', 'status',
        'issue_date', 'due_date', 'sent_date', 'paid_date', 'subtotal', 'tax', 'total'
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('service', 'company', 'contact', 'template')


class BillingViewSetGroup(SnippetViewSetGroup):
    menu_label = "Billing"
    menu_icon = "money"
    menu_order = 220  # After Services (210)
    items = (ContractTemplateViewSet, InvoiceTemplateViewSet,
             ContractViewSet, InvoiceViewSet)


@hooks.register('register_admin_urls')
def register_document_urls():
    return [
        path('crm/generate-contract/<int:contract_id>/',
             generate_contract_view, name='generate_contract'),
        path('crm/generate-invoice/<int:invoice_id>/',
             generate_invoice_view, name='generate_invoice'),
        path('crm/service-invoice/<int:service_id>/',
             create_service_invoice_view, name='create_service_invoice'),
    ]


def generate_contract_view(request, contract_id):
    contract = models.Contract.objects.get(id=contract_id)
    contract.generate_document()
    messages.success(
        request, f"Contract {contract.contract_id} generated successfully")
    return HttpResponseRedirect(reverse('wagtailadmin_snippets:edit', args=['crm', 'contract', contract.id]))


def generate_invoice_view(request, invoice_id):
    invoice = models.Invoice.objects.get(id=invoice_id)
    invoice.generate_document()
    messages.success(
        request, f"Invoice {invoice.invoice_id} generated successfully")
    return HttpResponseRedirect(reverse('wagtailadmin_snippets:edit', args=['crm', 'invoice', invoice.id]))


def create_service_invoice_view(request, service_id):
    service = models.Service.objects.get(id=service_id)
    try:
        invoice = service.create_invoice()
        invoice.generate_document()
        messages.success(
            request, f"Invoice created for service {service.name}")
        return HttpResponseRedirect(reverse('wagtailadmin_snippets:edit', args=['crm', 'invoice', invoice.id]))
    except Exception as e:
        messages.error(request, f"Error creating invoice: {str(e)}")
        return HttpResponseRedirect(reverse('wagtailadmin_snippets:edit', args=['crm', 'service', service.id]))


@hooks.register('register_page_listing_buttons')
def add_service_invoice_button(page, page_perms, is_parent=False):
    if isinstance(page, models.Service):
        yield {
            'url': reverse('create_service_invoice', args=[page.id]),
            'label': 'Create Invoice',
            'classname': 'button button-small button-secondary',
            'title': 'Create an invoice for this service',
        }


register_snippet(BillingViewSetGroup)
register_snippet(CRMViewSetGroup)
register_snippet(ServicesViewSetGroup)
