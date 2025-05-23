
from crm import models, utils


def run():
    active_campaigns = list(models.Campaign.objects.filter(is_active=True))
    for campaign in active_campaigns:
        utils.sync_campaign_is_active_end_date(campaign)
