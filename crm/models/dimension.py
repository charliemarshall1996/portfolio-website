import uuid
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from django.db import models
from django.urls import reverse


class Address(models.Model):
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True)
    town = models.CharField(max_length=100)
    region = models.CharField(max_length=100, blank=True)
    postcode = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="UK")

    def __str__(self):
        return f"{self.line1}, {self.town}, {self.postcode}"


class Email(models.Model):
    email = models.EmailField(unique=True)
    opted_out = models.BooleanField(default=False)
    bounced = models.BooleanField(default=False)
    last_emailed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email


class Painpoint(models.Model):
    vertical = ParentalKey(
        "Vertical", on_delete=models.CASCADE, related_name="painpoints"
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)


class PhoneNumber(models.Model):
    PHONE_TYPES = (
        ("mobile", "Mobile"),
        ("landline", "Landline"),
        ("work", "Work"),
        ("fax", "Fax"),
        ("other", "Other"),
    )

    phone_number = models.CharField(max_length=50)
    type = models.CharField(
        max_length=20, choices=PHONE_TYPES, null=True, blank=True)

    def __str__(self):
        return f"{self.phone_number} ({self.type})"


class SearchLocation(models.Model):
    TYPE_CHOICES = [("to", "Town"), ("pc", "Post Code")]
    type = models.CharField(max_length=2, default="to", choices=TYPE_CHOICES)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class SearchTerm(models.Model):
    vertical = ParentalKey(
        "Vertical",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="search_terms",
    )
    term = models.CharField(max_length=255)

    def __str__(self):
        return self.term


class Vertical(ClusterableModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Website(models.Model):
    url = models.URLField(unique=True)

    def __str__(self):
        return self.url


class LighthouseAnalysis(models.Model):
    website = models.ForeignKey(
        Website, on_delete=models.CASCADE, related_name="lighthouse_analyses"
    )
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
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
        verbose_name_plural = "Lighthouse Analyses"
