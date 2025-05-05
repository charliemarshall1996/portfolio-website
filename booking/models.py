from django.db import models
from django.utils import timezone


class Booking(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True, null=True)
    industry = models.CharField(max_length=50)
    email = models.EmailField()
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    end = models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        end = timezone.datetime.combine(self.date, self.time) + timezone.timedelta(
            minutes=15
        )
        self.end = end.time()
        super().save(*args, **kwargs)
