
from modelcluster.models import ClusterableModel
from django.db import models


class Contact(ClusterableModel):
    SALUTATION_CHOICES = [
        ("mr", "Mr."),
        ("mrs", "Mrs."),
        ("ms", "Ms."),
        ("dr", "Dr."),
    ]
    salutation = models.CharField(
        max_length=10, choices=SALUTATION_CHOICES, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True)
    linkedin = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Lead(ClusterableModel):
    SALUTATION_CHOICES = [
        ("mr", "Mr."),
        ("mrs", "Mrs."),
        ("ms", "Ms."),
        ("dr", "Dr."),
    ]

    STATUS_CHOICES = [
        ("aware", "Aware"),
        ("interested", "Interested"),
        ("engaged", "Engaged"),
        ("converted", "Converted"),
        ("cold", "Cold")
    ]

    salutation = models.CharField(
        max_length=10, choices=SALUTATION_CHOICES, blank=True, null=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
