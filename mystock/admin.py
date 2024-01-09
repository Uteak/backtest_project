
from django.contrib import admin

from .models import (
    StockDataYear,
    StockDataQuarter,
    StockData
)

admin.site.register(StockDataYear)
admin.site.register(StockDataQuarter)
admin.site.register(StockData)