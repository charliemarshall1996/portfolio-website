from django.db.models.signals import post_save
from django.dispatch import receiver
from . import models, utils


@receiver(post_save, sender=models.Contact)
def create_entity_for_contact(sender, instance, created, **kwargs):
    if not instance.entity:
        entity = models.Entity.objects.create(
            name=f"{instance.first_name} {instance.last_name}"
        )
        instance.entity = entity
        instance.save()


@receiver(post_save, sender=models.Company)
def create_entity_for_company(sender, instance, created, **kwargs):
    if not instance.entity:
        entity = models.Entity.objects.create(
            name=instance.name, is_company=True)
        instance.entity = entity
        instance.save()


@receiver(post_save, sender=models.Lead)
def create_entity_for_lead(sender, instance, created, **kwargs):
    if not instance.entity:
        entity = models.Entity.objects.create(
            name=f"{instance.first_name} {instance.last_name}"
        )
        instance.entity = entity
        instance.save()


@receiver(post_save, sender=models.Campaign)
def sync_search_params(sender, instance, created, **kwargs):
    utils.sync_campaign_is_active_end_date(instance)
    utils.sync_campaign_search_parameters(instance)


@receiver(post_save, sender=models.Website)
def normalize_website_url(sender, instance: models.Website, created, **kwargs):
    is_not_formatted = any([instance.url.startswith(
        "https://"), instance.url.startswith("http://"), instance.url.endswith("/")])
    if created or is_not_formatted:
        instance.url = utils.normalize_url(instance.url)
        instance.save(update_fields=["url"])


@receiver(post_save, sender=models.Email)
def normalize_email(sender, instance: models.Email, created, **kwargs):
    if created:
        instance.email = utils.normalize_email(instance.email)
        instance.save(update_fields=["email"])
