
from django.db.models.signals import post_save
from django.dispatch import receiver

from models import (ContactEmails,
                    ContactEntity,
                    ContactPhoneNumber,
                    EntityAddress,
                    EntityEmail,
                    EntityPhoneNumber,
                    EntityWebsite,
                    LeadEntity,
                    LeadEmail,
                    LeadPhoneNumber,
                    Contact,
                    Entity,
                    Lead,
                    Email,
                    PhoneNumber,
                    Address,
                    Website)


@receiver(post_save, Contact)
def make_contact_emails_on_contact_creation(sender, instance, created, **kwargs):
    if created:
        for email in list(Email.objects.all()):
            contact_email, created = ContactEmails.objects.get_or_create(contact=instance,
                                                                         email=email)
            if created:
                contact_email.save()


@receiver(post_save, Email)
def make_contact_emails_on_email_creation(sender, instance, created, **kwargs):
    if created:
        for contact in list(Contact.objects.all()):
            contact_email, created = ContactEmails.objects.get_or_create(email=instance,
                                                                         contact=contact)
            if created:
                contact_email.save()
