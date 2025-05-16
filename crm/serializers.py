from rest_framework import serializers
from . import models


class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Website
        exclude = ("contact",)


class ContactSerializer(serializers.ModelSerializer):
    websites = WebsiteSerializer(many=True)

    class Meta:
        model = models.Client
        fields = "__all__"

    def create(self, validated_data):
        websites_data = validated_data.pop("websites", [])
        contact, created = models.Client.objects.get_or_create(
            **validated_data)
        contact.save()
        for website_data in websites_data:
            # Remove 'contact' if present in the incoming data
            website_data.pop("contact", None)
            website, created = models.Website.objects.get_or_create(
                contact=contact, url=website_data["url"]
            )
            website.save()
        return contact
