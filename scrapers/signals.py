from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models


@receiver(post_save, sender=models.SearchTerm)
def create_new_parameters_on_search_term_creation(sender, instance, created, **kwargs):
    if created:

        try:
            locations = list(models.Location.objects.all())
            for l in locations:
                parameter = models.SearchParameter(term=instance, location=l)
                parameter.save()
        except:
            pass


@receiver(post_save, sender=models.Location)
def create_new_parameters_on_search_term_creation(sender, instance, created, **kwargs):
    if created:

        try:
            terms = list(models.SearchTerm.objects.all())
            for t in terms:
                parameter = models.SearchParameter(term=t, location=instance)
                parameter.save()
        except:
            pass
