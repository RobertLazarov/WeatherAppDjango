from django.db import models


class SearchHistory(models.Model):
    city_name = models.CharField(max_length=80)
    temperature = models.FloatField()
    humidity = models.PositiveIntegerField()
    pressure = models.PositiveIntegerField()
    description = models.CharField(max_length=120)
    searched_at = models.DateTimeField(auto_now_add=True)


class Meta:
    ordering = ['-searched_at']
    indexes = [
    models.Index(fields=['-searched_at']),
]


def __str__(self) -> str:
    return f"{self.city_name} @ {self.searched_at:%Y-%m-%d %H:%M}"