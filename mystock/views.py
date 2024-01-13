from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from mystock.models import StockDataYear, StockDataQuarter, StockData
from mystock.backtest import BackTestClass
from django.views import View
from django.views.generic import TemplateView

    
class IndexView(View):
    
    def get(self, request, *args, **kwargs):
        
        StockList = StockData.objects.values_list('code', 'name')
        #dic = {'KpiCodeList' : KpiCodeList, 'stock_year_data_dict' : stock_year_data_dict, 'stock_quarter_data_dict' : stock_quarter_data_dict}
        return render(request, 'index.html', {'StockList' : StockList})

    def post(self, request, *args, **kwargs):
        select_code = request.POST.get('button_name')
        stock_code_name_list = StockData.objects.values_list('code', 'name')
        stock_year_data = StockDataYear.objects.filter(code=select_code)
        stock_quarter_data = StockDataQuarter.objects.filter(code=select_code)
        stock_financial_data = StockData.objects.filter(code=select_code)
        context = {
            'StockList': stock_code_name_list,
            'StockDataYear' : stock_year_data,
            'StockDataQuarter' : stock_quarter_data,
            'StockFinancialData' : stock_financial_data
        }
        return render(request, 'index.html', context)
    
class ChartsView(View):
    template_name = 'charts.html'
    
    def get(self, request, *args, **kwargs):  
        years = range(2000, 2024)
        months = range(1, 13)
        context = {
            'years': years,
            'months' : months,
        }
        return render(request, 'backtestboard.html', context)
    
    def post(self, request, *args, **kwargs):
        global select_company_names, select_company_codes
        
        roe = request.POST.get('roe')
        roa = request.POST.get('roa')
        pbr = request.POST.get('pbr')
        per = request.POST.get('per')
        debt_ratio = request.POST.get('debt_ratio')

        stock_data = StockData.objects.all()
        #print(roe, pbr, per, debt_ratio, dividend_yield, dividend_propensity)

        print(roe, roa, pbr, per, debt_ratio)
        select_company_names = []
        select_company_codes = []
        for data in stock_data:
            
            # data 값이 비어있을 경우 선택하지 않음 ex) lg화학
            if not data.roe and not data.roa and not data.pbr:
                continue
            
            # roe값이 입력이 되었고 입력 roe값이 해당 종목 roe값보다 크다면 선택하지 않음
            if roe and float(roe) > float(data.roe):
                continue
            
            # roa값이 입력이 되었고 입력 roa값이 해당 종목 roa값보다 크다면 선택하지 않음
            if roa and float(roa) > float(data.roa):
                continue
            
            # pbr값이 입력이 되었고 입력 pbr값이 해당 종목 pbr값보다 작다면 선택하지 않음
            if pbr and float(pbr) < float(data.pbr):
                continue
            
            # per값이 입력이 되었고 입력 per값이 해당 종목 per값보다 작다면 선택하지 않음 
            if per and float(per) < float(data.per):
                continue
            
            if float(data.per) < 0:
                continue
            
            # debt_ratio값이 입력이 되었고 입력 debt_ratio값이 해당 종목 per값보다 작다면 선택하지 않음 
            if debt_ratio and float(debt_ratio) > (float(data.debt_ratio)):
                continue
            
            select_company_names.append(data.name)
            select_company_codes.append(data.code)
            
        years = range(2000, 2024)
        months = range(1, 13)
        context = {
            'SelectCompany' : select_company_names,
            'years': years,
            'months' : months,
        }
        return render(request, 'backtestboard.html', context)
    

class TablesView(TemplateView):
    template_name = 'tables.html'
    

class ResultView(TemplateView):
    template_name = 'reuslt.html'

    def post(self, request, *args, **kwargs):
        start_year = request.POST.get('start_year')
        start_month = request.POST.get('start_month')
        end_year = request.POST.get('end_year')  # Corrected to 'end_year'
        end_month = request.POST.get('end_month')
        
        start_month = start_month if len(start_month) == 2 else '0' + start_month
        end_month = end_month if len(end_month) == 2 else '0' + end_month
        start_data = start_year + '-' + start_month
        end_data = end_year + '-' + end_month
        
        back_test = BackTestClass(select_company_codes, select_company_names, start_data, end_data)
        # 전체 누적 수익률 그래프
        _accumulate_graph = back_test.accumulate_graph()
        _graph_list = back_test.return_graph()

        return_total_graph = _graph_list[-1]
        # 각 종목별 수익률 그래프
        return_graph_list = _graph_list[:-1]
        context = {
            'accumulate_graph' : _accumulate_graph,
            'return_total_graph' : return_total_graph,
            'images_and_names': zip(return_graph_list, select_company_names),
        }
        return render(request, 'result.html', context)
    
# def charts(request):
#     # pass
#     # return HttpResponse("main index")
#     return render(request, 'charts.html')