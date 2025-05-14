# crm/signals.py
from django.apps import apps
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from crm.models import Contact, Website

AnalysisWebsite = apps.get_model("website", "Website")

Email = apps.get_model("website", "Email")


@receiver(post_save, sender=Website)
def create_website_for_contact(sender, instance, created, **kwargs):
    if created:
        AnalysisWebsite.objects.create(
            contact_id=instance.contact.id, url=instance.url, website_id=instance.id
        )
    else:
        website = AnalysisWebsite.objects.get(website_id=instance.id)
        website.url = instance.url
        website.contact_id = instance.contact.id
        website.save()


@receiver(post_save, sender=Contact)
def create_email_for_contact(sender, instance, created, **kwargs):
    if created and instance.email:
        email, created = Email.objects.get_or_create(email=instance.email)
        email.contact_id = instance.id
        email.email = instance.email
        email.save()


@receiver(post_delete, sender=Website)
def delete_website_for_contact(sender, instance, **kwargs):
    websites = list(
        AnalysisWebsite.objects.filter(
            contact_id=instance.contact.id, url=instance.url, website_id=instance.id
        )
    )

    for website in websites:
        website.delete()


@receiver(post_delete, sender=Contact)
def delete_website_for_contact(sender, instance, **kwargs):
    websites = list(AnalysisWebsite.objects.filter(contact_id=instance.contact.id))
    for website in websites:
        website.delete()
