import FinanceDataReader as fdr
import dart_fss as dart
import requests
import json

class FinancialAnalysis:
    def __init__(self, api_key, stock_code, stock_count):
        self.api_key = api_key
        dart.set_api_key(api_key)
        self.corp_list = dart.get_corp_list()
        self.stock_code = stock_code
        self.stock_count = stock_count

    def get_market_capitalization(self):
        start_date = '2023-09-27'
        end_date = '2023-12-31'
        df = fdr.DataReader(self.stock_code, start_date, end_date)
        if not df.empty:
            closing_price = df['Close'].iloc[0]
        market_cap = closing_price * self.stock_count
        return market_cap

    def get_corp_code(self):
        dart.set_api_key(api_key=self.api_key)
        corp_info = self.corp_list.find_by_stock_code(self.stock_code)
        return str(corp_info)[1:9]

    def get_financial_data(self):
        corp_code = self.get_corp_code()
        
        # dart open api 데이터 크롤링
        url = f"https://opendart.fss.or.kr/api/fnlttSinglAcnt.json?crtfc_key={self.api_key}&corp_code={corp_code}&bsns_year=2023&reprt_code=11014"
        res = requests.get(url)
        jsondata = json.loads(res.text)
        financial_data = {}
        
        # 재무제표 데이터에서 필요한 데이터 추출
        for item in jsondata["list"]:
            account_name = item["account_nm"]
            relevant_accounts = ["유동자산", "비유동자산", "자산총계", "유동부채", "비유동부채", "부채총계", "자본금", "이익잉여금", "자본총계", "매출액", "영업이익", "법인세차감전 순이익", "당기순이익"]
            if account_name in relevant_accounts:
                amount = item["thstrm_amount"].replace(',', '')
                financial_data[account_name] = int(amount)
        
        # 2023 3분기 기준 시가총액 계산
        market_cap = self.get_market_capitalization()
        
        per = market_cap / financial_data["당기순이익"]
        pbr = market_cap / financial_data["자본총계"]
        roe = financial_data["당기순이익"] / financial_data["자본총계"]
        roa = financial_data["당기순이익"] / financial_data["자산총계"]
        debt_ratio = financial_data["부채총계"] / financial_data["자본총계"]
        
        result = {
            'market_cap' : market_cap,
            'per': per,
            'pbr': pbr,
            'roe': roe,
            'roa': roa,
            'debt_ratio': debt_ratio
        }
        return result
    
# api_key = 'b8d640fdc1449aec0c70f3f79b36671262b07676'
# stock_code = '005930'
# stock_count =  5969782550
# analysis = FinancialAnalysis(api_key, stock_code, stock_count)
# financial_data = analysis.get_financial_data()
# print(financial_data)