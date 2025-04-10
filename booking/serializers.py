from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['first_name', 'last_name', 'company',
                  'industry', 'email', 'description', 'date', 'time']
