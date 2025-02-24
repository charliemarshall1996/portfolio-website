import uuid
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Inquiry(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    linkedin_profile = models.URLField()
    description = models.TextField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_queue_link(self):
        return f"https://www.charlie-marshall.dev/free-sites/queue/{self.code}/"

    def queue_position(self):
        """Calculate the position in the queue (1-based index)."""
        return list(Inquiry.objects.filter(status="pending").order_by("created_at")).index(self) + 1

    def __str__(self):
        return self.name


class WebLink(models.Model):
    inquiry = models.ForeignKey(
        Inquiry, related_name="links", on_delete=models.CASCADE)
    url = models.URLField()


class Review(models.Model):
    name = models.CharField(max_length=255)
    review = models.TextField()
    positives = models.TextField()
    improvements = models.TextField()
    rating = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
