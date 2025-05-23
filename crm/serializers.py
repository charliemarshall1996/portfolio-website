
import logging

from rest_framework import serializers

from . import models, utils

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class CampaignSearchParameterSerializer(serializers.ModelSerializer):
    campaign_pk = serializers.SerializerMethodField(
        method_name="get_campaign_pk")
    location_pk = serializers.SerializerMethodField(
        method_name="get_location_pk")
    vertical_pk = serializers.SerializerMethodField(
        method_name="get_vertical_pk")
    search_term_pk = serializers.SerializerMethodField(
        method_name="get_search_term_pk")

    class Meta:
        model = models.CampaignSearchParameter
        fields = [
            "id", "campaign", "location", "search_term", "last_run",
            "campaign_pk", "location_pk", "vertical_pk", "search_term_pk"
        ]

    def get_campaign_pk(self, obj):
        return obj.campaign.pk

    def get_location_pk(self, obj):
        logger.debug("Getting location pk...")
        logger.debug("Param location: %s", obj.location)
        campaign_locations = models.CampaignSearchLocation.objects.filter(
            campaign=obj.campaign
        )
        logger.debug("Campaign locations: %s", len(campaign_locations))
        name_to_pk = {
            cl.location.name: cl.location.pk for cl in campaign_locations
        }
        logger.debug("Campaign location mapping: %s", name_to_pk)
        return name_to_pk.get(obj.location, "0")

    def get_vertical_pk(self, obj):
        campaign = obj.campaign
        vertical = campaign.vertical
        return vertical.pk

    def get_search_term_pk(self, obj):
        campaign = obj.campaign
        vertical = campaign.vertical
        search_term = models.SearchTerm.objects.get(
            vertical=vertical, term=obj.search_term)
        return search_term.pk
