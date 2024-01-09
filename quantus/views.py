from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


# from django.http import HttpResponse, HttpResponseNotFound
# from django.shortcuts import render, redirect
# from bs4 import BeautifulSoup
# from mystock.models import StockDataYear, StockDataQuarter

# import csv
# import os
# import re
# import requests
# import pandas as pd
# import sys
# import io

# #sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
# #sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

# def Kpi200_code():
#     KpiCodeList = []
#     BaseUrl = 'http://finance.naver.com/sise/entryJongmok.nhn?&page='

#     for i in range(1, 21):
#         url = BaseUrl + str(i)
#         r = requests.get(url)
#         #response.content.decode('euc-kr')
#         soup = BeautifulSoup(r.content.decode('euc-kr'), 'lxml')
#         items = soup.find_all('td', {'class': 'ctg'})

#         for item in items:
#             txt = item.a.get('href') # https://finance.naver.com/item/main.nhn?code=006390
#             k = re.search('[\d]+', txt) ## 정규표현식 사용. [\d] 숫자표현, + : 반복
#             if k:
#                 code = k.group()
#                 name = item.text
#                 KpiCodeList.append([code, name])

#     return KpiCodeList

# def index(request):
    
    # if request.method == 'GET':
    #     KpiCodeList = Kpi200_code()
    #     # images = Photo.objects.all()
    #     # labelList = LabelList.objects.all()
    #     # print(labelList)
        
    #     for _code, _name in KpiCodeList:
    #         stock_data_year = StockDataYear(code = _code, name = _name, period = "2022")
    #         stock_data_quarter = StockDataQuarter(code = _code, name = _name, period = "2022")
    #         stock_data_year.save()
    #         stock_data_quarter.save()
            
    # return render(request, 'index.html')
# def charts(request):
#     # pass
#     # return HttpResponse("main index")
#     return render(request, 'charts.html')