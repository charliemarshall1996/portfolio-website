import uuid
from django.db import models
from django.contrib.sites.models import Site
from django.urls import reverse

# Create your models here.


class Website(models.Model):
    contact_id = models.PositiveIntegerField()
    website_id = models.PositiveIntegerField()
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url


class Analysis(models.Model):
    website = models.ForeignKey(
        Website, on_delete=models.CASCADE, related_name="analyses")
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
        return reverse('website:audit_view', args=[self.access_token])

    def full_url(self):
        from django.contrib.sites.models import Site
        domain = Site.objects.get_current().domain
        return f"https://{domain}{self.get_absolute_url()}"

    full_url.short_description = "Access URL"

    def __str__(self):
        return self.website.url

    class Meta:
        verbose_name_plural = "Analyses"
