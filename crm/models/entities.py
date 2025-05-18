
from uuid import uuid4
from django.db import models


class Entity(models.Model):
    # Can be "Jane Smith", or "Acme Ltd"
    uuid = models.UUIDField(default=uuid4)
    vertical = models.ForeignKey(
        'crm.Vertical', on_delete=models.SET_NULL, null=True
    )
    location = models.ForeignKey(
        'crm.SearchLocation', on_delete=models.SET_NULL, null=True
    )
    search_term = models.ForeignKey(
        'crm.SearchTerm', on_delete=models.SET_NULL, null=True
    )
    campaign = models.ForeignKey(
        'crm.Campaign', on_delete=models.SET_NULL, null=True
    )
    name = models.CharField(max_length=255)
    is_company = models.BooleanField(default=False)
    emails = models.ManyToManyField('crm.Email', through='crm.EntityEmail')
    phone_numbers = models.ManyToManyField(
        'crm.PhoneNumber', through='crm.EntityPhoneNumber')
    websites = models.ManyToManyField(
        'crm.Website', through='crm.EntityWebsite')
    addresses = models.ManyToManyField('crm.Address', through='EntityAddress')
    leads = models.ManyToManyField('crm.Lead', through='crm.LeadEntity')
    contacts = models.ManyToManyField(
        'crm.Contact', through='crm.ContactEntity')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CompanyProfile(models.Model):
    entity = models.OneToOneField('crm.Entity', on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=100)
    headquarters = models.ForeignKey(
        'crm.Address', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.entity.name
