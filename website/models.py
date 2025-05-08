import uuid
from django.db import models

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

    def __str__(self):
        return self.website.url
