from django.db import models, transaction
from django.utils import timezone
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


def sync_campaign_search_parameters(campaign):
    search_term = campaign.vertical.search_term
    current_locations = set(
        campaign.campaignsearchlocation_set.values_list(
            "search_location_id", flat=True)
    )

    existing_params = CampaignSearchParameter.objects.filter(campaign=campaign)
    existing_map = {p.location_id: p for p in existing_params}

    for location_id in current_locations:
        if location_id in existing_map:
            param = existing_map[location_id]
            if not param.is_active:
                param.is_active = True
                param.save(update_fields=["is_active"])
        else:
            CampaignSearchParameter.objects.create(
                campaign=campaign,
                search_term=search_term,
                location_id=location_id,
                is_active=True,
            )

    for location_id, param in existing_map.items():
        if param.is_active and location_id not in current_locations:
            param.is_active = False
            param.save(update_fields=["is_active"])


def sync_campaign_is_active_end_date(campaign):
    if timezone.now() > timezone.timedelta(campaign.end_date) and campaign.is_active:
        campaign.is_active = False
        campaign.save(update_fields=["is_active"])


class Campaign(ClusterableModel):
    TYPE_CHOICES = [
        ("site_audit", "Website Audit"),
        ("client_analysis", "Client Analysis"),
    ]
    MEDIUM_CHOICES = [
        ("email", "Email"),
        ("phone", "Phone"),
        ("social_media", "Social Media"),
        ("direct_mail", "Direct Mail"),
    ]
    vertical = models.ForeignKey(
        "crm.Vertical", on_delete=models.SET_NULL, null=True, related_name="campaigns"
    )
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    medium = models.CharField(max_length=50, choices=MEDIUM_CHOICES)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        transaction.on_commit(
            lambda: sync_campaign_search_parameters(self))
        transaction.on_commit(
            lambda: sync_campaign_is_active_end_date(self)
        )


class CampaignSearchParameter(models.Model):
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name="search_parameters"
    )
    location = models.CharField(max_length=200)
    search_term = models.CharField(max_length=200)
    last_run = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)


class CampaignEmailContent(models.Model):
    PART_CHOICES = [
        ("greeting", "Greeting"),
        ("intro", "Intro"),
        ("score", "Score"),
        ("closing", "Closing"),
        ("farewell", "Farewell"),
    ]
    METRIC_CHOICES = [
        ("acc", "Accessibility"),
        ("bp", "Best Practices"),
        ("per", "Performance"),
        ("seo", "SEO"),
    ]
    CORE_SCORE_BAND_CHOICES = [(50, "low"), (90, "mid"), (100, "high")]
    campaign = ParentalKey(
        Campaign, on_delete=models.CASCADE, related_name="email_content"
    )
    part = models.CharField(max_length=50, choices=PART_CHOICES)
    metric = models.CharField(
        max_length=3, choices=METRIC_CHOICES, blank=True, null=True
    )
    core_score_band = models.IntegerField(
        choices=CORE_SCORE_BAND_CHOICES, null=True)
    active = models.BooleanField(default=True)
    message = models.TextField()


class CampaignSearchLocation(models.Model):
    campaign = ParentalKey(
        Campaign, on_delete=models.CASCADE, related_name="search_locations"
    )
    location = models.ForeignKey(
        "crm.SearchLocation", on_delete=models.CASCADE)
