from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Orderable

from crm import services


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
    type = models.CharField(
        max_length=50, choices=TYPE_CHOICES, default="site_audit")
    medium = models.CharField(
        max_length=50, choices=MEDIUM_CHOICES, default="email")
    description = models.TextField(blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CampaignMetric(Orderable):
    ACTION_CHOICES = [
        ("s", "Sent"),
        ("d", "Deliveries"),
        ("o", "Opens"),
        ("1", "First Opens"),
        ("l", "Link Clicks"),
        ("b", "Bounces"),
        ("x", "Opt-Outs"),
        ("+", "Leads Added")
    ]

    campaign = ParentalKey(
        Campaign, on_delete=models.CASCADE, related_name="metrics")
    action = models.CharField(max_length=1, choices=ACTION_CHOICES)
    value = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["campaign", "action"]


class CampaignSearchParameter(ClusterableModel):
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name="search_parameters"
    )
    location = models.CharField(max_length=200)
    location_pk = models.IntegerField(blank=True, null=True)
    search_term = models.CharField(max_length=200)
    search_term_pk = models.IntegerField(blank=True, null=True)
    last_run = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


class CampaignSearchParameterMetric(Orderable):
    ACTION_CHOICES = [
        ("s", "Sent"),
        ("d", "Deliveries"),
        ("o", "Opens"),
        ("1", "First Opens"),
        ("l", "Link Clicks"),
        ("b", "Bounces"),
        ("x", "Opt-Outs"),
        ("+", "Leads Added")
    ]

    campaign_search_parameter = ParentalKey(
        CampaignSearchParameter, on_delete=models.CASCADE, related_name="metrics"
    )
    action = models.CharField(max_length=1, choices=ACTION_CHOICES)
    value = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["campaign_search_parameter", "action"]


class EmailContent(ClusterableModel):
    STAGE_CHOICES = [("i", "Initial"), ("f", "Follow-Up")]
    campaign = ParentalKey(
        Campaign, on_delete=models.CASCADE, related_name="email_content"
    )

    stage = models.CharField(max_length=1, choices=STAGE_CHOICES, default="i")
    subject = models.TextField(blank=True)
    greeting = models.TextField(blank=True)
    intro = models.TextField(blank=True)
    main = models.TextField(blank=True, null=True)
    closing = models.TextField(blank=True)
    farewell = models.TextField(blank=True)
    link_text = models.TextField(blank=True, null=True)

    panels = [
        FieldPanel("stage"),
        FieldPanel("greeting"),
        FieldPanel("intro"),
        FieldPanel("main"),
        InlinePanel("bullet_contents", label="Bullet Points"),
        FieldPanel("closing"),
        FieldPanel("farewell"),
    ]

    def __str__(self):
        return f"EmailContent for {self.campaign.pk}"

    def get_full_email(self, first_name, link, metric_score_map=None):
        if self.stage == "i" and first_name and metric_score_map and link:
            return self._get_initial_email(first_name, metric_score_map, link)
        else:
            return self._get_follow_up_email(first_name, link)

    def _get_initial_email(self, first_name, metric_score_map, link):
        # Collect bullet contents matching any metric/score_range pair
        bullet_items = []
        for metric, score_range in metric_score_map.items():
            bullets = self.bullet_contents.filter(
                metric=metric, score_range=score_range)
            bullet_items.extend(bullets)

        return services.retrieve_initial_email(first_name, link, link,
                                               bullet_items, self.greeting, self.intro,
                                               self.closing, self.farewell)

    def _get_follow_up_email(self, first_name, link):
        return services.retrieve_follow_up_email(first_name, link, link,
                                                 self.main, self.greeting, self.intro,
                                                 self.closing, self.farewell)


class BulletContent(Orderable):
    email_content = ParentalKey(
        EmailContent, on_delete=models.CASCADE, related_name="bullet_contents"
    )

    METRIC_CHOICES = [
        ("accessibility", "Accessibility"),
        ("best_practices", "Best Practices"),
        ("seo", "SEO"),
        ("performance", "Performance"),
    ]
    SCORE_RANGE_CHOICES = [
        ("l", "Low"),
        ("m", "Mid"),
        ("h", "High"),
    ]

    metric = models.CharField(max_length=20, choices=METRIC_CHOICES)
    score_range = models.CharField(max_length=1, choices=SCORE_RANGE_CHOICES)
    content = models.TextField()

    panels = [
        FieldPanel("metric"),
        FieldPanel("score_range"),
        FieldPanel("content"),
    ]

    def __str__(self):
        return f"{self.metric} {self.score_range}"


class CampaignSearchLocation(Orderable):
    campaign = ParentalKey(
        Campaign, on_delete=models.CASCADE, related_name="search_locations"
    )
    location = models.ForeignKey(
        "crm.SearchLocation", on_delete=models.CASCADE)


class EmailContentMetric(Orderable):
    ACTION_CHOICES = [
        ("s", "Sent"),
        ("d", "Deliveries"),
        ("o", "Opens"),
        ("1", "First Opens"),
        ("l", "Link Clicks"),
        ("b", "Bounces"),
        ("x", "Opt-Outs"),
    ]

    email_content = ParentalKey(
        EmailContent, on_delete=models.CASCADE, related_name="metrics"
    )
    action = models.CharField(max_length=1, choices=ACTION_CHOICES)
    value = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["email_content", "action"]
