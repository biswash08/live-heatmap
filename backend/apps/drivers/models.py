from django.db import models


class Driver(models.Model):
    id = models.BigAutoField(primary_key=True)
    driver_id = models.CharField(max_length=64, unique=True)
    city_id = models.CharField(max_length=32, blank=True)
    availability_status = models.CharField(max_length=32, default='offline')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    current_h3_cell = models.CharField(max_length=32, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'drivers'
