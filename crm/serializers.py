
from rest_framework import serializers
from . import models


class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Website
        exclude = ('contact',)


class ContactSerializer(serializers.ModelSerializer):
    websites = WebsiteSerializer(many=True)

    class Meta:
        model = models.Contact
        fields = "__all__"

    def create(self, validated_data):
        websites_data = validated_data.pop('websites', [])
        contact = models.Contact.objects.create(**validated_data)
        for website_data in websites_data:
            # Remove 'contact' if present in the incoming data
            website_data.pop('contact', None)
            models.Website.objects.get_or_create(
                contact=contact,
                url=website_data['url']
            )
        return contact
