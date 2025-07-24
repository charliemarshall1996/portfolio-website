from django.db import models

# Create your models here.


class Vertical(models.Model):
    name = models.CharField()
    description = models.TextField()


class Contact(models.Model):
    STATUS_CHOICES = [
        ("lead", "Lead"),
        ("client", "Client"),
        ("former", "Former")
    ]
    first_name = models.CharField()
    last_name = models.CharField()
    email = models.EmailField()
    email_opt_out = models.BooleanField(default=False)
    phone = models.CharField()
    website = models.URLField()
    company = models.CharField()
    vertical = models.ForeignKey(Vertical, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=6, choices=STATUS_CHOICES, default="lead")


class Communication(models.Model):
    MEDIUM_CHOICES = [
        ("phone", "Phone"),
        ("email", "Email"),
        ("video call", "Video Call")
    ]
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    medium = models.CharField(max_length=11, default="email")
    made_on = models.DateTimeField()
    notes = models.TextField(null=True, blank=True)
