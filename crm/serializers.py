
from rest_framework import serializers
from . import models


class WebsiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Website
        fields = "__all__"


class ContactSerializer(serializers.ModelSerializer):
    websites = WebsiteSerializer(many=True)

    class Meta:
        model = models.Contact
        fields = "__all__"

    def create(self, validated_data):
        websites_data = validated_data.pop('websites', [])
        contact = models.Contact.objects.create(**validated_data)
        for website_data in websites_data:
            models.Website.objects.create(contact=contact, **website_data)
        return contact
