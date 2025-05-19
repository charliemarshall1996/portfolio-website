
from django.db.models import signals
from django.dispatch import receiver

from models import SearchTerm, Campaign, CampaignSearchParemeter


@receiver(signals.post_save, Campaign)
def create_search_parameters_on_campaign_save(sender, instance, **kwargs):
    for term in list(instance.vertical.search_terms):
        for loc in list(instance.locations):
            search_param, created = CampaignSearchParemeter.objects.get_or_create(campaign=instance,
                                                                                  location=loc, search_term=term)
            search_param.save()
