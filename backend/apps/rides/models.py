import uuid

from django.db import models


def generate_request_id() -> str:
    return f"ride-{uuid.uuid4().hex[:12]}"


class RideRequest(models.Model):
    id = models.BigAutoField(primary_key=True)
    request_id = models.CharField(max_length=64, unique=True, default=generate_request_id)
    pickup_address = models.CharField(max_length=255)
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    destination_address = models.CharField(max_length=255)
    destination_latitude = models.FloatField()
    destination_longitude = models.FloatField()
    vehicle_type = models.CharField(max_length=32, default='car')
    estimated_fare = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    surge_multiplier = models.DecimalField(max_digits=4, decimal_places=2, default=1.0)
    status = models.CharField(max_length=32, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'rides'
        ordering = ['-created_at']
