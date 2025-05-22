from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from django.db import models


class Entity(ClusterableModel):
    name = models.CharField(max_length=200)
    notes = models.TextField(blank=True, null=True)
    is_company = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Company(ClusterableModel):
    name = models.CharField(max_length=200, blank=True, null=True)
    registration_number = models.CharField(max_length=200, blank=True, null=True)
    entity = models.OneToOneField(
        Entity, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.name


class Contact(models.Model):
    SALUTATION_CHOICES = [
        ("mr", "Mr."),
        ("mrs", "Mrs."),
        ("ms", "Ms."),
        ("dr", "Dr."),
    ]
    salutation = models.CharField(
        max_length=3, choices=SALUTATION_CHOICES, blank=True, null=True
    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    job_title = models.CharField(max_length=200, blank=True)
    linkedin = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    entity = models.OneToOneField(
        Entity, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Lead(models.Model):
    SALUTATION_CHOICES = [
        ("mr", "Mr."),
        ("mrs", "Mrs."),
        ("ms", "Ms."),
        ("dr", "Dr."),
    ]

    STATUS_CHOICES = [
        ("aware", "Aware"),
        ("interested", "Interested"),
        ("engaged", "Engaged"),
        ("converted", "Converted"),
        ("cold", "Cold"),
    ]
    salutation = models.CharField(
        max_length=10, choices=SALUTATION_CHOICES, blank=True, null=True
    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    entity = models.OneToOneField(
        Entity, on_delete=models.CASCADE, null=True, blank=True
    )


class EntityEmail(models.Model):
    entity = ParentalKey(Entity, on_delete=models.CASCADE)
    email = models.ForeignKey("crm.Email", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["entity", "email"]


class EntityAddress(models.Model):
    entity = ParentalKey(Entity, on_delete=models.CASCADE)
    address = models.ForeignKey("crm.Address", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["entity", "address"]


class EntityPhoneNumber(models.Model):
    entity = ParentalKey(Entity, on_delete=models.CASCADE)
    phone_number = models.ForeignKey("crm.PhoneNumber", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["entity", "phone_number"]


class EntityWebsite(models.Model):
    entity = ParentalKey(Entity, on_delete=models.CASCADE)
    website = models.ForeignKey("crm.Website", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["entity", "website"]


class EntitySearchLocation(models.Model):
    entity = ParentalKey(Entity, on_delete=models.CASCADE)
    location = models.ForeignKey("crm.SearchLocation", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["entity", "location"]


class EntityVertical(models.Model):
    entity = ParentalKey(Entity, on_delete=models.CASCADE)
    vertical = models.ForeignKey("crm.Vertical", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["entity", "vertical"]


class CompanyContact(models.Model):
    company = ParentalKey(Entity, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["company", "contact"]
