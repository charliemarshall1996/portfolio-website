from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Company(models.Model):

    STATUS_CHOICES = [
        ("le", "Lead"),
        ("pr", "Prospect"),
        ("cl", "Client"),
        ("fo", "Former")
    ]

    INDUSTRY_CHOICES = [
        ("ed", "Education"),
        ("lo", "Logistics"),
        ("fs", "Financial Services"),
        ("mk", "Marketing")
    ]
    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=2, choices=INDUSTRY_CHOICES)
    website = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} | {self.industry}"


class Contact(models.Model):

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    company = models.ForeignKey(
        Company, related_name="contacts", on_delete=models.SET_NULL, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} | {self.company}"


class Interaction(models.Model):

    MEDIUM_CHOICES = [
        ('ph', 'Phone'),
        ('em', 'Email'),
        ('vc', 'Video Call'),
        ('li', 'LinkedIn')
    ]
    contact = models.ForeignKey(
        Contact, related_name="interactions", on_delete=models.SET_NULL, blank=True, null=True)
    company = models.ForeignKey(
        Company, related_name="interactions", on_delete=models.CASCADE)
    medium = models.CharField(max_length=2, choices=MEDIUM_CHOICES)
    summary = models.CharField(max_length=255)
    detail = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    follow_up = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.contact.first_name}, {self.company.name} | {self.date}, {self.time}"


class Project(models.Model):

    STATUS_CHOICES = [
        ("di", "Discovery"),
        ("de", "Project Definition"),
        ("co", "Conceptualization"),
        ("id", "Initial Development"),
        ("it", "Iterative Development"),
        ("co", "Completed"),
        ("ho", "On Hold"),
        ("ca", "Cancelled")
    ]

    title = models.CharField(max_length=255)
    company = models.ForeignKey(
        Company, related_name="projects", on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    value = models.DecimalField(
        blank=True, null=True, decimal_places=2, max_digits=8)
    start_date = models.DateField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} | {self.company}"


class Task(models.Model):

    PRIORITY_CHOICES = [
        ("l", "Low"),
        ("m", "Medium"),
        ("h", "High")
    ]

    title = models.CharField(max_length=255)
    project = models.ForeignKey(
        Project, related_name="tasks", blank=True, null=True, on_delete=models.CASCADE)
    company = models.ForeignKey(
        Company, related_name="tasks", blank=True, null=True, on_delete=models.CASCADE)
    due_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES)
    notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} | {self.company.name} | {self.due_date}"
