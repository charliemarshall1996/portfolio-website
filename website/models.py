from django.db import models

# Create your models here.


class Website(models.Model):
    contact_id = models.PositiveIntegerField()
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Analysis(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
