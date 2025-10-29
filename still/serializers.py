from rest_framework import serializers
from .models import DynamicData

class DynamicDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DynamicData
        fields = '__all__'
