from rest_framework import serializers

from . import models


class CampaignSearchParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CampaignSearchParameter
        fields = ["id", "campaign", "location", "search_term", "last_run"]
