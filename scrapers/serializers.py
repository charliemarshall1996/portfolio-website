from rest_framework import serializers
from . import models


class SearchParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SearchParameter
        fields = [
            'id',
            'term',
            'location',
            'last_run_thomson',
            'last_run_freeindex'
        ]
