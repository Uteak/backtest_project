from mystock.management.commands.parsing import crawled_data_to_model_save
from mystock.management.commands.FinancialAnalysis import FinancialAnalysis
from mystock.models import StockDataYear, StockDataQuarter, StockData

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        
        self.stdout.write('크롤링을 시작합니다...')
        existing_codes = set(StockData.objects.values_list('code', flat=True))
        stock_list, stock_year_data_dict, stock_quarter_data_dict = crawled_data_to_model_save()
        
        for _code, _name, _stock_count in stock_list:
            if _code not in existing_codes:                    
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

                api_key = 'b8d640fdc1449aec0c70f3f79b36671262b07676'
                analysis = FinancialAnalysis(api_key, _code, _stock_count)
                try:
                    #analysis = FinancialAnalysis(api_key, _code, _stock_count)
                    financial_data = analysis.get_financial_data()
                    print('success :', _code, _name)
                    _market_cap = financial_data['market_cap']
                    _per = round(financial_data['per'], 2)
                    _pbr = round(financial_data['pbr'], 2)
                    _roe = round(financial_data['roe'] * 100, 2)
                    _roa = round(financial_data['roa'] * 100, 2)
                    _debt_ratio= round(financial_data['debt_ratio'] * 100, 2)
                    stock_data = StockData(
                            code=_code, name=_name, stock_count = _stock_count, 
                            market_capitalization = _market_cap, per = _per, pbr = _pbr, roe = _roe,
                            roa = _roa, debt_ratio = _debt_ratio,
                        )
                    stock_data.save()
                except Exception as e: 
                    print("오류 발생:", e)
                    stock_data = StockData(
                            code=_code, name=_name, stock_count = _stock_count, 
                            market_capitalization = None, per = None, pbr = None, roe = None,
                            roa = None, debt_ratio = None,
                        )
                    stock_data.save()                 
                    continue 

        self.stdout.write(self.style.SUCCESS('크롤링이 완료되었습니다.'))
        
        
        
# existing_codes = set(StockData.objects.values_list('code', flat=True))
# stock_list, stock_year_data_dict, stock_quarter_data_dict = crawled_data_to_model_save()
# for _code, _name, _stock_count in stock_list:
#     if _code not in existing_codes:                    
        
#         for items in stock_year_data_dict[_code]:
#             _year, _pbr, _roe, _per, _dividend_yield, _dividend_propensity, _debt_ratio = items
                
#             stock_data_year = StockDataYear(
#                 code=_code, name=_name, year=_year, roe=_roe, per=_per, 
#                 pbr=_pbr, debt_ratio=_debt_ratio, dividend_yield=_dividend_yield, dividend_propensity=_dividend_propensity
#             )
#             stock_data_year.save()
            
#         for items in stock_quarter_data_dict[_code]:
#             _quarter, _pbr, _roe, _per, _dividend_yield, _dividend_propensity, _debt_ratio = items
        
#             stock_data_quarter = StockDataQuarter(
#                 code=_code, name=_name, quarter=_quarter, roe=_roe, per=_per, 
#                 pbr=_pbr, debt_ratio=_debt_ratio, dividend_yield=_dividend_yield, dividend_propensity=_dividend_propensity
#             )
#             stock_data_quarter.save()
        
#         api_key = 'b8d640fdc1449aec0c70f3f79b36671262b07676'
#         analysis = FinancialAnalysis(api_key, _code, _stock_count)
#         try:
#             #analysis = FinancialAnalysis(api_key, _code, _stock_count)
#             financial_data = analysis.get_financial_data()
#             print('success :', _code, _name)
#             _market_cap = financial_data['market_cap']
#             _per = round(financial_data['per'], 2)
#             _pbr = round(financial_data['pbr'], 2)
#             _roe = round(financial_data['roe'] * 100, 2)
#             _roa = round(financial_data['roa'] * 100, 2)
#             _debt_ratio= round(financial_data['debt_ratio'] * 100, 2)
#             stock_data = StockData(
#                     code=_code, name=_name, stock_count = _stock_count, 
#                     market_capitalization = _market_cap, per = _per, pbr = _pbr, roe = _roe,
#                     roa = _roa, debt_ratio = _debt_ratio,
#                 )
#             stock_data.save()
#         except Exception as e: 
#             print("오류 발생:", e)
#             stock_data = StockData(
#                     code=_code, name=_name, stock_count = _stock_count, 
#                     market_capitalization = None, per = None, pbr = None, roe = None,
#                     roa = None, debt_ratio = None,
#                 )
#             stock_data.save()                 
#             continue 