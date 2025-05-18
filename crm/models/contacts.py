
from django.db import models


class Contact(models.Model):
    SALUTATION_CHOICES = [
        ("mr", "Mr."),
        ("mrs", "Mrs."),
        ("ms", "Ms."),
        ("dr", "Dr."),
    ]
    salutation = models.CharField(
        max_length=10, choices=SALUTATION_CHOICES, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True)
    linkedin = models.URLField(blank=True)
    emails = models.ManyToManyField('crm.Email', through='crm.ContactEmail')
    phone_numbers = models.ManyToManyField(
        'crm.PhoneNumber', through='crm.ContactPhoneNumber')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Lead(models.Model):
    STATUS_CHOICES = [
        ("aware", "Aware"),
        ("interested", "Interested"),
        ("engaged", "Engaged"),
        ("converted", "Converted"),
        ("cold", "Cold")
    ]
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=100)
    emails = models.ManyToManyField('crm.Email', through='crm.LeadEmail')
    phone_numbers = models.ManyToManyField('crm.PhoneNumber',
                                           through='crm.LeadPhoneNumber')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
