from django.db import models


class City(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    name = models.CharField(max_length=128)
    country = models.CharField(max_length=64, default='Nepal')
    default_h3_resolution = models.PositiveSmallIntegerField(default=8)

    class Meta:
        app_label = 'cities'
