from django.db import models


class AuthAuditLog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.CharField(max_length=64, db_index=True)
    action = models.CharField(max_length=64)

    class Meta:
        app_label = 'authentication'
