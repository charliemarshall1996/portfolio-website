from django.db import models

# Create your models here.


class SearchTerm(models.Model):
    term = models.CharField(max_length=255)

    def __str__(self):
        return self.term


class Location(models.Model):
    LOCATION_TYPES = [
        ("pc", "Post Code"),
        ("to", "Town")
    ]
    type = models.CharField(max_length=2, choices=LOCATION_TYPES)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SearchParameter(models.Model):
    term = models.ForeignKey(SearchTerm, models.CASCADE)
    location = models.ForeignKey(Location, models.CASCADE)
    live = models.BooleanField(default=True)
    last_run_freeindex = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.term.term} | {self.location.name}"
