from django.db import models
from .models import StockDataQuarter, StockDataYear, StockData

class StockDataForm(models.Model):
    class Meta:
        model = StockData
        fields = ['code', 'name']
        
class StockDataYearForm(models.Model):
    class Meta:
        model = StockDataYear
        fields = ['code', 'name', 'year', 'ROA', 'ROE', 'PER', 'PBR', 'DebtRatio', 'DividendYield', 'DividendPropensity']

class StockDataQuarterForm(models.Model):
    class Meta:
        model = StockDataQuarter
        fields = ['code', 'name', 'quarter', 'ROA', 'ROE', 'PER', 'PBR', 'DebtRatio', 'DividendYield', 'DividendPropensity']