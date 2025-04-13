from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone


class Visitor(models.Model):
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(null=True, blank=True)
    referrer = models.URLField(null=True, blank=True)
    first_visited = models.DateTimeField(default=timezone.now)
    last_visited = models.DateTimeField(auto_now=True)
    page_views = models.PositiveIntegerField(default=0)
    visited_pages = models.JSONField(default=list)
    browser = models.CharField(max_length=100, blank=True)
    os = models.CharField(max_length=100, blank=True)
    device = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.ip_address} - {self.session_key}"
