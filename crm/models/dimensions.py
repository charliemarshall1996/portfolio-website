
from django.db import models


class Address(models.Model):
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True)
    town = models.CharField(max_length=100)
    region = models.CharField(max_length=100, blank=True)
    postcode = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='UK')

    def __str__(self):
        return f"{self.line1}, {self.town}, {self.postcode}"


class Email(models.Model):
    email = models.EmailField(unique=True)
    last_emailed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email


class PhoneNumber(models.Model):
    PHONE_TYPES = (
        ('mobile', 'Mobile'),
        ('landline', 'Landline'),
        ('work', 'Work'),
        ('fax', 'Fax'),
        ('other', 'Other'),
    )

    phone_number = models.CharField(max_length=50)
    type = models.CharField(
        max_length=20, choices=PHONE_TYPES, null=True, blank=True)

    def __str__(self):
        return f"{self.phone_number} ({self.type})"


class SearchLocation(models.Model):
    campaign = models.ForeignKey(
        "crm.Campaign", on_delete=models.CASCADE, related_name='search_locations')
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ("name", "campaign")

    def __str__(self):
        return self.name


class SearchTerm(models.Model):
    vertical = models.ForeignKey(
        "Vertical", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="search_terms")
    term = models.CharField(max_length=255)

    def __str__(self):
        return self.term


class Vertical(models.Model):
    name = models.CharField(max_length=255)
    pain_points = models.TextField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Website(models.Model):
    url = models.URLField()

    def __str__(self):
        return self.url
