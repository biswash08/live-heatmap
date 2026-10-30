from django.db import models


class RideRequest(models.Model):
    id = models.BigAutoField(primary_key=True)
    request_id = models.CharField(max_length=64, unique=True)
    status = models.CharField(max_length=32, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'rides'
