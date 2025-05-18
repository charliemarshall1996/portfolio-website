
from django.db import models


class ContactEmails(models.Model):
    contact = models.ForeignKey(
        "crm.Contact", on_delete=models.CASCADE)
    email = models.ForeignKey(
        "crm.Email", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("contact", "email")
        verbose_name_plural = "contact_emails"


class ContactEntity(models.Model):
    contact = models.ForeignKey(
        "crm.Contact", on_delete=models.CASCADE)
    entity = models.ForeignKey(
        "crm.Entity", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("contact", "entity")
        verbose_name_plural = "contact_entities"


class ContactPhoneNumber(models.Model):
    contact = models.ForeignKey(
        "crm.Contact", on_delete=models.CASCADE)
    phone_number = models.ForeignKey(
        "crm.PhoneNumber", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("contact", "phone_number")
        verbose_name_plural = "contact_phone_numbers"


class EntityAddress(models.Model):
    entity = models.ForeignKey(
        "crm.Entity", on_delete=models.CASCADE)
    address = models.ForeignKey(
        "crm.Address", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("entity", "address")
        verbose_name_plural = "entity_addresses"


class EntityEmail(models.Model):
    entity = models.ForeignKey(
        "crm.Entity", on_delete=models.CASCADE)
    email = models.ForeignKey(
        "crm.Email", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("entity", "email")
        verbose_name_plural = "entity_emails"


class EntityPhoneNumber(models.Model):
    entity = models.ForeignKey(
        "crm.Entity", on_delete=models.CASCADE)
    phone_number = models.ForeignKey(
        "crm.PhoneNumber", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("entity", "phone_number")
        verbose_name_plural = "entity_phone_numbers"


class EntityWebsite(models.Model):
    entity = models.ForeignKey(
        "crm.Entity", on_delete=models.CASCADE)
    website = models.ForeignKey(
        "crm.Website", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("entity", "website")
        verbose_name_plural = "entity_websites"


class LeadEntity(models.Model):
    lead = models.ForeignKey("crm.Lead",
                             on_delete=models.CASCADE)
    entity = models.ForeignKey(
        "crm.Entity", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("lead", "entity")
        verbose_name_plural = "lead_entities"


class LeadEmail(models.Model):
    lead = models.ForeignKey("crm.Lead",
                             on_delete=models.CASCADE)
    email = models.ForeignKey(
        "crm.Email", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("lead", "email")
        verbose_name_plural = "lead_emails"


class LeadPhoneNumber(models.Model):
    lead = models.ForeignKey("crm.Lead",
                             on_delete=models.CASCADE)
    phone_number = models.ForeignKey(
        "crm.PhoneNumber", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("lead", "phone_number")
        verbose_name_plural = "lead_phone_numbers"
