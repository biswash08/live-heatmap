from rest_framework import serializers

from .models import RideRequest


class RideRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideRequest
        fields = [
            'id',
            'request_id',
            'pickup_address',
            'pickup_latitude',
            'pickup_longitude',
            'destination_address',
            'destination_latitude',
            'destination_longitude',
            'vehicle_type',
            'estimated_fare',
            'surge_multiplier',
            'status',
            'created_at',
        ]
        read_only_fields = ['id', 'request_id', 'status', 'created_at']

    def validate_pickup_latitude(self, value):
        if not (-90.0 <= float(value) <= 90.0):
            raise serializers.ValidationError('pickup latitude is out of range.')
        return value

    def validate_pickup_longitude(self, value):
        if not (-180.0 <= float(value) <= 180.0):
            raise serializers.ValidationError('pickup longitude is out of range.')
        return value

    def validate_destination_latitude(self, value):
        if not (-90.0 <= float(value) <= 90.0):
            raise serializers.ValidationError('destination latitude is out of range.')
        return value

    def validate_destination_longitude(self, value):
        if not (-180.0 <= float(value) <= 180.0):
            raise serializers.ValidationError('destination longitude is out of range.')
        return value
