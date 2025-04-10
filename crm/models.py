"""Data models for all CRM-related records.

Data description for contained models:
- Company: a lead, prospect, client or former-client company.
- Contact: a person working for a lead, prospect, client or former-client company.
- Interaction: an interaction had with a lead, prospect, client or former-client company
and/or contact.
"""

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Company(models.Model):
    """Django model of a lead, prospect, client or former-client company."""
    STATUS_CHOICES = [
        ("le", "Lead"),
        ("pr", "Prospect"),
        ("cl", "Client"),
        ("fo", "Former"),
    ]

    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):  # noqa: D105
        return f"{self.name} | {self.industry}"


class Contact(models.Model):
    """Django representation of a person working for a company."""
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    company = models.ForeignKey(
        Company,
        related_name="contacts",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    email = models.EmailField(blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):  # noqa: D105
        return f"{self.first_name} {self.last_name} | {self.company}"


class Interaction(models.Model):
    """Django representation of an interaction with a Contact and/or Company."""
    MEDIUM_CHOICES = [
        ("ph", "Phone"),
        ("em", "Email"),
        ("vc", "Video Call"),
        ("li", "LinkedIn"),
    ]
    contact = models.ForeignKey(
        Contact,
        related_name="interactions",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    company = models.ForeignKey(
        Company, related_name="interactions", on_delete=models.CASCADE
    )
    medium = models.CharField(max_length=2, choices=MEDIUM_CHOICES)
    summary = models.CharField(max_length=255)
    detail = models.TextField()
    timestamp = models.DateTimeField()
    follow_up = models.DateField(blank=True, null=True)

    def __str__(self):  # noqa: D105
        return (
            f"{self.contact.first_name}, {self.company.name} | {self.date}, {self.time}"
        )
