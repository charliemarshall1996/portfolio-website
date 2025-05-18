
from django.urls import reverse
import uuid
from django.db import models


class Campaign(models.Model):
    TYPE_CHOICES = [
        ('site_audit', 'Website Audit'),
        ('client_analysis', 'Client Analysis'),
    ]
    MEDIUM_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('social_media', 'Social Media'),
        ('direct_mail', 'Direct Mail'),
    ]
    vertical = models.ForeignKey(
        'crm.Vertical', on_delete=models.SET_NULL, null=True, related_name='campaigns')
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    medium = models.CharField(max_length=50, choices=MEDIUM_CHOICES)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CampaignSearchParemeter(models.Model):
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name='search_parameters')
    search_term = models.ForeignKey(
        'crm.SearchTerm', on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(
        'crm.SearchLocation', on_delete=models.SET_NULL, null=True, blank=True)
    last_run = models.DateTimeField(null=True, blank=True)


class CampaignEmailContent(models.Model):
    PART_CHOICES = [
        ("greeting", "Greeting"),
        ("intro", "Intro"),
        ("score", "Score"),
        ("closing", "Closing"),
        ("farewell", "Farewell")
    ]
    METRIC_CHOICES = [
        ("acc", "Accessibility"),
        ("bp", "Best Practices"),
        ("per", "Performance"),
        ("seo", "SEO")
    ]
    CORE_SCORE_BAND_CHOICES = [
        (50, "low"),
        (90, "mid"),
        (100, "high")
    ]
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name='messages')
    part = models.CharField(max_length=50, choices=PART_CHOICES)
    metric = models.CharField(
        max_length=3, choices=METRIC_CHOICES, blank=True, null=True)
    core_score_band = models.IntegerField(
        choices=CORE_SCORE_BAND_CHOICES, null=True)
    active = models.BooleanField(default=True)
    message = models.TextField()

    def __str__(self):
        return f"{self.metric} - {self.get_core_score_band_display()}"
