from django.db import models
from django.utils.timezone import now

class Sources(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    api_key = models.TextField(blank=True)
    url = models.CharField(max_length=300, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Wooi(models.Model):
    title = models.CharField(max_length=100)
    handle = models.CharField(blank=False, max_length=100)
    description = models.TextField(blank=True)
    source_api = models.ForeignKey(Sources, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    legal = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    nav_link = models.CharField(blank=True, max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    historical_available = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class HistoricalData(models.Model):
    spot = models.ForeignKey(Wooi, on_delete=models.CASCADE)
    timestamp = models.CharField(blank=False, max_length=100)
    gust = models.FloatField(default=0)
    wind = models.FloatField(default=0)
    created = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return (self.timestamp)