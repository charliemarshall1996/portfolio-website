
from rest_framework import serializers
from . import models


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contact
        fields = [
            'id',
            'salutation',
            'first_name',
            'last_name',
            'company',
            'position',
            'email',
            'phone',
            'mobile',
            'linkedin',
            'status',
            'notes',
            'created_at',
            'updated_at',
        ]
