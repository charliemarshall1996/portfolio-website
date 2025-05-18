
from django.db import models


class Engagement(models.Model):
    campaign = models.ForeignKey(
        "crm.Campaign", on_delete=models.CASCADE)
    entity = models.ForeignKey("crm.Entity", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class OpenedEmailEngagement(models.Model):
    engagement = models.ForeignKey(Engagement, on_delete=models.CASCADE)
    sent_campaign_email = models.ForeignKey(
        "crm.SentCampaignEmail", on_delete=models.CASCADE)
    opened_at = models.DateTimeField(auto_now_add=True)
    n = models.PositiveIntegerField(default=1)


class ResponseEmailEngagement(models.Model):
    engagement = models.ForeignKey(Engagement, on_delete=models.CASCADE)
    sent_campaign_email = models.ForeignKey(
        "crm.SentCampaignEmail", on_delete=models.CASCADE)
    received_at = models.DateTimeField()
    content = models.TextField()
    is_positive = models.BooleanField(default=False)


class LinkEngagement(models.Model):
    engagement = models.ForeignKey(Engagement, on_delete=models.CASCADE)
    sent_campaign_email = models.ForeignKey(
        "crm.SentCampaignEmail", on_delete=models.CASCADE, null=True, blank=True)
    viewed_at = models.DateTimeField()
    time_spent_seconds = models.FloatField(null=True)
