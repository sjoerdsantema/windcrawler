from django.contrib import admin
from .models import Wooi, Sources, HistoricalData

admin.site.register(Wooi)
admin.site.register(Sources)
admin.site.register(HistoricalData)
