from django.db import models

# Create your models here.


class Booking(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    date = models.DateField()
    time = models.CharField(max_length=5, choices=[], blank=False)
    email = models.EmailField()
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('date', 'time')

    def __str__(self):
        return f"{self.first_name} | {self.company} | {self.date}, {self.time}"
