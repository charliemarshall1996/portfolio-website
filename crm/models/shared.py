
from modelcluster.fields import ParentalKey
from wagtail.models import Orderable
from django.db import models


class CampaignSearchLocations(Orderable):
    campaign = ParentalKey(
        "crm.Campaign", on_delete=models.CASCADE, related_name="campaign_search_locations")
    location = models.ForeignKey(
        "crm.SearchLocation", on_delete=models.CASCADE
    )


class ContactEmail(Orderable):
    contact = ParentalKey(
        "crm.Contact", on_delete=models.CASCADE, related_name="contact_emails")
    email = models.ForeignKey(
        "crm.Email", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("contact", "email")
        verbose_name_plural = "contact_emails"


class ContactEntity(Orderable):
    contact = ParentalKey(
        "crm.Contact", on_delete=models.CASCADE, related_name="contact_entities")
    entity = models.ForeignKey(
        "crm.Entity", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("contact", "entity")
        verbose_name_plural = "contact_entities"


class ContactPhoneNumber(Orderable):
    contact = ParentalKey(
        "crm.Contact", on_delete=models.CASCADE, related_name="contact_phone_numbers")
    phone_number = models.ForeignKey(
        "crm.PhoneNumber", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("contact", "phone_number")
        verbose_name_plural = "contact_phone_numbers"


class EntityAddress(Orderable):
    entity = ParentalKey(
        "crm.Entity", on_delete=models.CASCADE, related_name="entity_addresses")
    address = models.ForeignKey(
        "crm.Address", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("entity", "address")
        verbose_name_plural = "entity_addresses"


class EntityContact(Orderable):
    entity = ParentalKey(
        "crm.Entity", on_delete=models.CASCADE, related_name="entity_contacts")
    contact = models.ForeignKey(
        "crm.Contact", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("contact", "entity")
        verbose_name_plural = "contact_entities"


class EntityLead(Orderable):
    lead = models.ForeignKey("crm.Lead",
                             on_delete=models.CASCADE)
    entity = ParentalKey(
        "crm.Entity", on_delete=models.CASCADE, related_name="entity_leads")

    class Meta:
        unique_together = ("lead", "entity")
        verbose_name_plural = "lead_entities"


class EntityEmail(Orderable):
    entity = ParentalKey(
        "crm.Entity", on_delete=models.CASCADE, related_name="entity_emails")
    email = models.ForeignKey(
        "crm.Email", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("entity", "email")
        verbose_name_plural = "entity_emails"


class EntityPhoneNumber(Orderable):
    entity = ParentalKey(
        "crm.Entity", on_delete=models.CASCADE, related_name="entity_phone_numbers")
    phone_number = models.ForeignKey(
        "crm.PhoneNumber", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("entity", "phone_number")
        verbose_name_plural = "entity_phone_numbers"


class EntityWebsite(Orderable):
    entity = ParentalKey(
        "crm.Entity", on_delete=models.CASCADE, related_name="entity_websites")
    website = models.ForeignKey(
        "crm.Website", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("entity", "website")
        verbose_name_plural = "entity_websites"


class LeadEntity(Orderable):
    lead = ParentalKey("crm.Lead",
                       on_delete=models.CASCADE, related_name="lead_entities")
    entity = models.ForeignKey(
        "crm.Entity", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("lead", "entity")
        verbose_name_plural = "lead_entities"


class LeadEmail(Orderable):
    lead = ParentalKey("crm.Lead",
                       on_delete=models.CASCADE, related_name="lead_emails")
    email = models.ForeignKey(
        "crm.Email", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("lead", "email")
        verbose_name_plural = "lead_emails"


class LeadPhoneNumber(Orderable):
    lead = ParentalKey("crm.Lead",
                       on_delete=models.CASCADE, related_name="lead_phone_numbers")
    phone_number = models.ForeignKey(
        "crm.PhoneNumber", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("lead", "phone_number")
        verbose_name_plural = "lead_phone_numbers"
