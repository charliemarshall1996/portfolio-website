from django.db import models

# Create your models here.


class Vertical(models.Model):
    name = models.CharField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Contact(models.Model):
    STATUS_CHOICES = [
        ("lead", "Lead"),
        ("client", "Client"),
        ("former", "Former")
    ]
    first_name = models.CharField(blank=True, null=True)
    last_name = models.CharField(blank=True, null=True)
    email = models.EmailField(unique=True)
    email_opt_out = models.BooleanField(default=False)
    phone = models.CharField(blank=True, null=True)
    website = models.URLField(unique=True)
    company = models.CharField(blank=True, null=True)
    vertical = models.ForeignKey(Vertical, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=6, choices=STATUS_CHOICES, default="lead")

    def __str__(self):
        if self.first_name:
            if self.last_name:
                if self.company:
                    return f"{self.first_name} {self.last_name}, {self.company}"
                else:
                    return f"{self.first_name} {self.last_name}"
            elif self.company:
                return f"{self.first_name}, {self.company}"
            else:
                return self.first_name
        elif self.company:
            return self.company
        else:
            return self.pk


class Communication(models.Model):
    MEDIUM_CHOICES = [
        ("phone", "Phone"),
        ("email", "Email"),
        ("video call", "Video Call")
    ]
    DIRECTION_CHOICES = [
        ("in", "Inbound"),
        ("out", "Outbound")
    ]
    COMMUNICATION_TYPE_CHOICES = [
        ("cold", "Cold"),
        ("reply", "Reply"),
        ("discovery", "Discovery"),
        ("other", "Other")
    ]

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    medium = models.CharField(max_length=11, default="email")
    direction = models.CharField(
        max_length=3, default="out", choices=DIRECTION_CHOICES)
    communication_type = models.CharField(max_length=9, default="cold",
                                          choices=COMMUNICATION_TYPE_CHOICES)
    subject = models.CharField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    made_on = models.DateTimeField()
    notes = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ["contact", "made_on"]

    def __str__(self):
        return f"{self.contact}, {self.made_on}"
