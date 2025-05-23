from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


class Outreach(ClusterableModel):
    MEDIUM_CHOICES = [
        ("p", "Phone"),
        ("e", "Email"),
        ("a", "Address"),
        ("w", "Website"),
    ]
    campaign_search_parameter = models.ForeignKey(
        "crm.CampaignSearchParameter", on_delete=models.CASCADE
    )
    date = models.DateTimeField()
    medium = models.CharField(
        max_length=1, choices=MEDIUM_CHOICES, default="e")


class OutreachEmail(models.Model):
    outreach = ParentalKey(
        Outreach, on_delete=models.CASCADE, related_name="email")
    email = models.ForeignKey("crm.Email", on_delete=models.CASCADE)


class OutreachWebsite(models.Model):
    outreach = ParentalKey(
        Outreach, on_delete=models.CASCADE, related_name="website")
    website = models.ForeignKey("crm.Website", on_delete=models.CASCADE)
