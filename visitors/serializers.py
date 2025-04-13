
from .models import Visitor
from rest_framework import serializers


class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = '__all__'
