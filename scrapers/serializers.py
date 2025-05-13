from rest_framework import serializers
from . import models


class SearchParameterSerializer(serializers.ModelSerializer):
    term = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    class Meta:
        model = models.SearchParameter
        fields = [
            'id',
            'term',
            'location',
            'last_run_thomson',
            'last_run_freeindex'
        ]

    def get_term(self, obj):
        return obj.term.term if obj.term else None

    def get_location(self, obj):
        return obj.location.name if obj.location else None
