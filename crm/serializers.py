from rest_framework import serializers

from . import models


class CampaignSearchParameterSerializer(serializers.ModelSerializer):
    campaign_pk = serializers.SerializerMethodField()
    location_pk = serializers.SerializerMethodField()
    vertical_pk = serializers.SerializerMethodField()
    search_term_pk = serializers.SerializerMethodField()

    class Meta:
        model = models.CampaignSearchParameter
        fields = [
            "id", "campaign", "location", "search_term", "last_run",
            "campaign_pk", "location_pk", "vertical_pk", "search_term_pk"
        ]

    def get_campaign_pk(self, obj):
        return obj.campaign.pk

    def get_location_pk(self, obj):
        campaign_locations = models.CampaignSearchLocation.objects.filter(
            campaign=obj.campaign
        )
        name_to_pk = {
            cl.location.name: cl.location.pk for cl in campaign_locations
        }
        return name_to_pk.get(obj.location)

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
