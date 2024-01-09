from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from mystock.models import StockDataYear, StockDataQuarter, StockData
from django.views import View
from django.views.generic import TemplateView
from mystock.parsing import Kpi200_code, crawled_data_to_model_save
import os
import re
import requests
import pandas as pd
import sys
import io

# def index(request):

#     if request.method == 'GET':
#         existing_codes = set(StockDataYear.objects.values_list('code', flat=True))
#         if not existing_codes:
#             KpiCodeList = Kpi200_code()
            
#             for _code, _name in KpiCodeList:
#                 if _code not in existing_codes:
#                     stock_data_year = StockDataYear(code=_code, name=_name, period="2022", roe=None, per=None, pbr=None, debt_ratio=None, dividend_yield=None, dividend_propensity=None)
#                     stock_data_quarter = StockDataQuarter(code=_code, name=_name, period="2022", roe=None, per=None, pbr=None, debt_ratio=None, dividend_yield=None, dividend_propensity=None)
#                     stock_data_year.save()
#                     stock_data_quarter.save()
#                 else:
#                     print(f"Code {_code} already exists in database.")
            
#         return render(request, 'index.html')
    
class IndexView(View):
    
    def get(self, request, *args, **kwargs):
        
        existing_codes = set(StockData.objects.values_list('code', flat=True))
        if not existing_codes:
            
            KpiCodeList, stock_year_data_dict, stock_quarter_data_dict = crawled_data_to_model_save()
            for _code, _name in KpiCodeList:
                if _code not in existing_codes:
                    stock_data = StockData(
                        code=_code, name=_name
                    )
                    stock_data.save()
                    
                    for items in stock_year_data_dict[_code]:
                        _year, _pbr, _roe, _per, _dividend_yield, _dividend_propensity, _debt_ratio = items
                            
                        stock_data_year = StockDataYear(
                            code=_code, name=_name, year=_year, roe=_roe, per=_per, 
                            pbr=_pbr, debt_ratio=_debt_ratio, dividend_yield=_dividend_yield, dividend_propensity=_dividend_propensity
                        )
                        stock_data_year.save()
                        
                    for items in stock_quarter_data_dict[_code]:
                        _quarter, _pbr, _roe, _per, _dividend_yield, _dividend_propensity, _debt_ratio = items
                    
                        stock_data_quarter = StockDataQuarter(
                            code=_code, name=_name, quarter=_quarter, roe=_roe, per=_per, 
                            pbr=_pbr, debt_ratio=_debt_ratio, dividend_yield=_dividend_yield, dividend_propensity=_dividend_propensity
                        )
                        stock_data_quarter.save()

                else:
                    print(f"Code {_code} already exists in database.")

        #stock_year_data_dict
        #tock_quarter_data_dict
        #print(KpiCodeList)
        StockList = StockData.objects.values_list('code', 'name')
        #dic = {'KpiCodeList' : KpiCodeList, 'stock_year_data_dict' : stock_year_data_dict, 'stock_quarter_data_dict' : stock_quarter_data_dict}
        return render(request, 'index.html', {'StockList' : StockList})

    def post(self, request, *args, **kwargs):
        select_code = request.POST.get('button_name')
        StockList = StockData.objects.values_list('code', 'name')
        stock_year_data = StockDataYear.objects.filter(code=select_code)
        stock_quarter_data = StockDataQuarter.objects.filter(code=select_code)
        return render(request, 'index.html', {'StockList' : StockList, 'StockDataYear' : stock_year_data, 'StockDataQuarter' : stock_quarter_data})
    
class ChartsView(View):
    template_name = 'charts.html'
    
    def get(self, request, *args, **kwargs):  
        return render(request, 'charts.html')
    
    def post(self, request, *args, **kwargs):
        roe = request.POST.get('roe')
        pbr = request.POST.get('pbr')

        print(roe, pbr)
        
        return render(request, 'charts.html')
    


class TablesView(TemplateView):
    template_name = 'tables.html'
# def charts(request):
#     # pass
#     # return HttpResponse("main index")
#     return render(request, 'charts.html')