
from django.db import models


class SentCampaignEmail(models.Model):
    TYPE_CHOICES = [
        (1, "Initial"),
        (2, "Follow-Up")
    ]
    OPT_OUT_AFTER_CHOICES = [
        ("first", "First Email"),
        ("second", "Follow-Up Email"),
        ("link view", "Link Viewed")
    ]
    campaign = models.ForeignKey(
        "crm.Campaign", on_delete=models.CASCADE,
        related_name='sent_campaign_emails',
        null=True)
    campaign_email_content = models.ForeignKey("crm.CampaignEmailContent",
                                               on_delete=models.CASCADE,
                                               related_name="sent")
    to = models.ForeignKey("crm.Email", on_delete=models.CASCADE)
    type = models.IntegerField(choices=TYPE_CHOICES)
    sent_at = models.DateTimeField(auto_now_add=True)
    opt_out_after = models.CharField(
        max_length=50, choices=OPT_OUT_AFTER_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.to.email} {self.get_type_display()}, {self.sent_at}"


class OptedOutEmail(models.Model):
    sent_campaign_email = models.ForeignKey(
        SentCampaignEmail, models.SET_NULL, null=True)
    email = models.OneToOneField("crm.Email", on_delete=models.CASCADE)
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email.email


class BouncedEmail(models.Model):
    TYPE_CHOICES = [
        ("hard", "Hard"),
        ("soft", "Soft")
    ]
    sent_campaign_email = models.ForeignKey(
        SentCampaignEmail, models.SET_NULL, null=True, blank=True)
    email = models.OneToOneField("crm.Email", on_delete=models.CASCADE)
    type = models.CharField(max_length=4, choices=TYPE_CHOICES, default="hard")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email.email
