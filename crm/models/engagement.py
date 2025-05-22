from django.db import models
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey


class Engagement(ClusterableModel):
    outreach = ParentalKey("crm.Outreach", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class EmailEngagement(models.Model):
    TYPE_CHOICES = [("o", "Opened"), ("x", "Opt-Out"), ("b", "Bounced")]

    engagement = ParentalKey(Engagement, on_delete=models.CASCADE)
    email = models.EmailField()
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)


class WebEngagement(models.Model):
    TYPE_CHOICES = [("l", "Link Clicked"), ("b", "Booking Made")]
    engagement = ParentalKey(Engagement, on_delete=models.CASCADE)
    url = models.URLField()
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
