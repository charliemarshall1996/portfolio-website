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
    registration_number = models.CharField(
        max_length=200, blank=True, null=True)
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
        ("a", "Aware"),
        ("i", "Interested"),
        ("e", "Engaged"),
        ("c", "Converted"),
        ("x", "Cold"),
    ]
    salutation = models.CharField(
        max_length=10, choices=SALUTATION_CHOICES, blank=True, null=True
    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, null=True, blank=True
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    campaign = models.PositiveIntegerField(null=True, blank=True)
    campaign_search_param = models.PositiveIntegerField(null=True, blank=True)
    entity = models.OneToOneField(
        Entity, on_delete=models.CASCADE, null=True, blank=True
    )


class EntityEmail(models.Model):
    entity = ParentalKey(Entity, on_delete=models.CASCADE,
                         related_name="emails")
    email = models.ForeignKey("crm.Email", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["entity", "email"]


class EntityAddress(models.Model):
    entity = ParentalKey(Entity, on_delete=models.CASCADE,
                         related_name="addresses")
    address = models.ForeignKey("crm.Address", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["entity", "address"]


class EntityPhoneNumber(models.Model):
    entity = ParentalKey(Entity, on_delete=models.CASCADE,
                         related_name="phone_numbers")
    phone_number = models.ForeignKey(
        "crm.PhoneNumber", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["entity", "phone_number"]


class EntityWebsite(models.Model):
    entity = ParentalKey(Entity, on_delete=models.CASCADE,
                         related_name="websites")
    website = models.ForeignKey("crm.Website", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["entity", "website"]


class EntitySearchLocation(models.Model):
    entity = ParentalKey(
        Entity, on_delete=models.CASCADE, related_name="search_locations"
    )
    location = models.ForeignKey(
        "crm.SearchLocation", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["entity", "location"]


class EntityVertical(models.Model):
    entity = ParentalKey(Entity, on_delete=models.CASCADE,
                         related_name="verticals")
    vertical = models.ForeignKey("crm.Vertical", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["entity", "vertical"]


class EntitySearchTerm(models.Model):
    entity = ParentalKey(Entity, on_delete=models.CASCADE,
                         related_name="search_terms")
    search_term = models.ForeignKey("crm.SearchTerm", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["entity", "search_term"]


class EntityCampaign(models.Model):
    entity = ParentalKey(Entity, on_delete=models.CASCADE,
                         related_name="campaigns")
    campaign = models.ForeignKey("crm.Campaign", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["entity", "campaign"]


class CompanyContact(models.Model):
    company = ParentalKey(Company, on_delete=models.CASCADE,
                          related_name="contacts")
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["company", "contact"]
