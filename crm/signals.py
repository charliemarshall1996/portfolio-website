from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Contact, Company, Lead, Entity


@receiver(post_save, sender=Contact)
def create_entity_for_contact(sender, instance, created, **kwargs):
    if not instance.entity:
        entity = Entity.objects.create(
            name=f"{instance.first_name} {instance.last_name}"
        )
        instance.entity = entity
        instance.save()


@receiver(post_save, sender=Company)
def create_entity_for_company(sender, instance, created, **kwargs):
    if not instance.entity:
        entity = Entity.objects.create(name=instance.name, is_company=True)
        instance.entity = entity
        instance.save()


@receiver(post_save, sender=Lead)
def create_entity_for_lead(sender, instance, created, **kwargs):
    if not instance.entity:
        entity = Entity.objects.create(
            name=f"{instance.first_name} {instance.last_name}"
        )
        instance.entity = entity
        instance.save()
