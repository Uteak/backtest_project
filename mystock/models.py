from django.db import models
from django.contrib.auth.models import User
    
class StockData(models.Model):
    
    code = models.CharField(max_length=30, db_index=True)
    name = models.CharField(max_length=30)  # 인덱스 추가
    stock_count = models.IntegerField()
    
    market_capitalization = models.IntegerField(null=True)
    roe = models.CharField(max_length=20, null=True)
    roa = models.CharField(max_length=20, null=True)
    per = models.CharField(max_length=20, null=True)
    pbr = models.CharField(max_length=20, null=True)
    debt_ratio = models.CharField(max_length=20, null=True)
    
    def __str__(self):
        return self.name

class StockDataYear(models.Model):
    
    code = models.CharField(max_length=30, db_index=True) 
    name = models.CharField(max_length=30)  
    year = models.CharField(max_length=15)

    roe = models.CharField(max_length=20, null=True)
    per = models.CharField(max_length=20, null=True)
    pbr = models.CharField(max_length=20, null=True)
    debt_ratio = models.CharField(max_length=20, null=True)
    dividend_yield = models.CharField(max_length=20, null=True)
    dividend_propensity = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f"{self.name} - {self.year}"
        
class StockDataQuarter(models.Model):
    
    code = models.CharField(max_length=30, db_index=True) 
    name = models.CharField(max_length=30)  
    quarter = models.CharField(max_length=15)

    roe = models.CharField(max_length=20, null=True)
    per = models.CharField(max_length=20, null=True)
    pbr = models.CharField(max_length=20, null=True)
    debt_ratio = models.CharField(max_length=20, null=True)
    dividend_yield = models.CharField(max_length=20, null=True)
    dividend_propensity = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f"{self.name} - {self.quarter}"
