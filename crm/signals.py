# crm/signals.py
from django.apps import apps
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from crm.models import Contact, Website

AnalysisWebsite = apps.get_model('website', 'Website')


@receiver(post_save, sender=Website)
def create_website_for_contact(sender, instance, created, **kwargs):
    if created:
        AnalysisWebsite.objects.create(
            contact_id=instance.contact.id, url=instance.url, website_id=instance.id)
    else:
        website = AnalysisWebsite.objects.get(website_id=instance.id)
        website.url = instance.url
        website.contact_id = instance.contact.id


@receiver(post_delete, sender=Website)
def delete_website_for_contact(sender, instance, **kwargs):
    AnalysisWebsite.objects.delete(
        contact_id=instance.contact.id, url=instance.url, website_id=instance.id)


@receiver(post_delete, sender=Contact)
def delete_website_for_contact(sender, instance, **kwargs):
    AnalysisWebsite.objects.delete(contact_id=instance.contact.id)
