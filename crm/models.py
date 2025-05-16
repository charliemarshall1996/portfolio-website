"""Data models for all CRM-related records.

Data description for contained models:
- Company: a lead, prospect, client or former-client company.
- Contact: a person working for a lead, prospect, client or former-client company.
- Interaction: an interaction had with a lead, prospect, client or former-client company
and/or contact.
"""

from django.urls import reverse
import uuid
from modelcluster.models import ClusterableModel
from django.db import models

# Create your models here.


class Client(ClusterableModel):
    SALUTATION_CHOICES = [
        ("mr", "Mr."),
        ("mrs", "Mrs."),
        ("ms", "Ms."),
        ("dr", "Dr."),
    ]
    STATUS_CHOICES = [
        ("cl", "Client")
    ]
    salutation = models.CharField(
        max_length=10, choices=SALUTATION_CHOICES, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    linkedin = models.URLField(blank=True)
    status = models.CharField(
        max_length=2, choices=STATUS_CHOICES, default=STATUS_CHOICES[0]
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    search_term = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Location(models.Model):
    LOCATION_TYPE_CHOICES = [
        ("town", "Town"),
        ("postcode", "Postcode"),
    ]
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Vertical(models.Model):
    name = models.CharField(max_length=255)
    pain_points = models.TextField(blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SearchTerm(models.Model):
    veritcal = models.ForeignKey(
        Vertical, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="search_terms")
    term = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.term


class Campaign(models.Model):
    CAMPAIGN_TYPE_CHOICES = [
        ('site_audit', 'Website Audit'),
        ('client_analysis', 'Client Analysis'),
    ]

    MEDIUM_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('social_media', 'Social Media'),
        ('direct_mail', 'Direct Mail'),
    ]

    name = models.CharField(max_length=200)
    type = models.CharField(max_length=50, choices=CAMPAIGN_TYPE_CHOICES)
    medium = models.CharField(max_length=50, choices=MEDIUM_CHOICES)
    vertical = models.ForeignKey(
        Vertical, on_delete=models.SET_NULL, null=True, related_name='campaigns')

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
        SearchTerm, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True)
    last_run = models.DateTimeField(null=True, blank=True)


class Message(models.Model):
    MESSAGE_PART_CHOICES = [
        ("greeting", "Greeting"),
        ("intro", "Intro"),
        ("score", "Score"),
        ("closing", "Closing"),
        ("farewell", "Farewell")
    ]
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name='messages')
    part = models.CharField(max_length=50, choices=MESSAGE_PART_CHOICES)
    metric = models.CharField(max_length=50, blank=True, null=True)
    score_band = models.CharField(max_length=50, blank=True, null=True)
    active = models.BooleanField(default=True)
    message = models.TextField()

    def __str__(self):
        return f"{self.get_vertical_display()} - {self.metric} - {self.score_band}"


class Lead(models.Model):

    STATUS_CHOICES = [
        ('new', 'New'),
        ('aware', 'Aware'),
        ('interested', 'Interested'),
        ('engaged', 'Engaged'),
        ('converted', 'Converted'),
        ('cold', 'Cold')
    ]

    OPT_OUT_AFTER_CHOICES = [
        ('first_emailed', 'First Emailed'),
        ('follow_up_emailed', 'Follow Up Emailed'),
        ('audit_viewed', 'Audit Viewed'),
    ]

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, blank=True, unique=True)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=200, blank=True)

    vertical = models.ForeignKey(
        Vertical, on_delete=models.SET_NULL, null=True)
    search_term = models.ForeignKey(
        SearchTerm, on_delete=models.SET_NULL, null=True, blank=True)
    search_location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True)
    campaign = models.ForeignKey(
        Campaign, on_delete=models.SET_NULL, null=True, related_name='leads')
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    audit_url = models.URLField(blank=True)

    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='new')

    # Engagement
    first_emailed_on = models.DateTimeField(null=True, blank=True)
    email_bounced = models.BooleanField(default=False)
    email_opened = models.BooleanField(default=False)

    follow_up_emailed_on = models.DateTimeField(null=True, blank=True)
    follow_up_email_bounced = models.BooleanField(default=False)
    follow_up_email_opened = models.BooleanField(default=False)

    audit_viewed = models.BooleanField(default=False)
    call_booked = models.BooleanField(default=False)
    converted = models.BooleanField(default=False)
    opt_out = models.BooleanField(default=False)
    opt_out_after = models.CharField(
        max_length=50, choices=OPT_OUT_AFTER_CHOICES, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)


class CampaignMetric(models.Model):
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name='metrics')
    name = models.CharField(max_length=100)
    value = models.IntegerField(default=0)
    recorded_at = models.DateTimeField(auto_now_add=True)


class OptedOutEmails(models.Model):
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name='opted_out_emails')
    email = models.EmailField(max_length=200, unique=True)
    reason = models.TextField(blank=True)
    opt_out_after = models.CharField(
        max_length=50, choices=Lead.OPT_OUT_AFTER_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class CampaignEvent(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(blank=True, null=True)


# Create your models here.


class Website(models.Model):
    client = models.PositiveIntegerField(null=True, blank=True)
    lead = models.PositiveIntegerField(null=True, blank=True)
    campaign = models.PositiveIntegerField(null=True, blank=True)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url


class Analysis(models.Model):
    website = models.ForeignKey(
        Website, on_delete=models.CASCADE, related_name="analyses"
    )
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    access_token = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False)

    report_url = models.URLField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.report_url:
            self.report_url = self.full_url()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("website:audit_view", args=[self.access_token])

    def full_url(self):
        from django.contrib.sites.models import Site

        domain = Site.objects.get_current().domain
        return f"https://{domain}{self.get_absolute_url()}"

    full_url.short_description = "Access URL"

    def __str__(self):
        return self.website.url

    class Meta:
        verbose_name_plural = "Analyses"
