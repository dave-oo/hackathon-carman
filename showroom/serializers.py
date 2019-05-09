from rest_framework import serializers
from .models import Car


class CarSerializer(serializers.ModelSerializer):
    """
    Serialize cars from the car model
    """
    class Meta:
        model = Car
        fields = '__all__'
