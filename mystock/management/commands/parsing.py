from bs4 import BeautifulSoup
import re
import requests
import pandas as pd
import urllib.request as req
from stock_data import FinancialData
import FinanceDataReader as fdr
import math

def Kpi200_code():
    KpiCodeList = []
    BaseUrl = 'http://finance.naver.com/sise/entryJongmok.nhn?&page='

    for i in range(1, 21):
        url = BaseUrl + str(i)  
        resp = req.urlopen(url)
        soup = BeautifulSoup(resp, 'html.parser') 
        items = soup.find_all('td', {'class': 'ctg'})

        for item in items:
            txt = item.a.get('href') 
            k = re.search('[\d]+', txt) ##정규표현식 사용. [\d] 숫자표현, + : 반복
            if k:
                code = k.group()
                name = item.text
                KpiCodeList.append([code, name])

    return KpiCodeList

def get_stock_count(company_name, df_krx):
    
    df_krx = df_krx
    stock_code = df_krx[df_krx['Name'] == company_name]['Stocks'].values
    
    return stock_code[0]

def dataframe_to_list(dataframe):
    data_list = dataframe.drop('주요재무정보', axis=1).values.tolist()[0]
    data_list = list(zip(dataframe.columns[1:], data_list))
    data_list = [(col, None if (isinstance(val, float) and math.isnan(val)) or val == '-' else val) for col, val in data_list]
    return data_list

   
def crawled_data_to_model_save():
    # 한국 거래소 상장 종목 전체 불러오기
    df_krx = fdr.StockListing('KRX')
    KpiCodeList = Kpi200_code()
    stock_list = []
    for code, name in KpiCodeList:
        stock_code = get_stock_count(name, df_krx)
        stock_list.append([code, name, stock_code])
        
    stock_year_data_dict = dict()
    stock_quarter_data_dict = dict()
    
    for _code, _name, stock_count in stock_list:
        code = _code
        print(code)
        URL = f"https://finance.naver.com/item/main.nhn?code={code}" 
        # URL = f"https://finance.naver.com/item/main.nhn?" 
        response = requests.get(URL)
        #html = response.content.decode('utf-8','replace') 
        dataframes = pd.read_html(response.content.decode('euc-kr'))
        df = pd.DataFrame(dataframes[3])
        df.columns = df.columns.droplevel([0, 2])

        # df_stock_year = df.iloc[:, :5]
        # df_name = df.iloc[:, :1]
        # df_stock_quarter = df.iloc[:, 5:]
        # df_stock_quarter = pd.concat([df_name, df_stock_quarter], axis=1)
        
        #pbr_data = df.loc[df['주요재무정보'] == 'PBR(배)']
        #pbr_data_list = pbr_data.drop('주요재무정보', axis=1).values.tolist()[0]
        #pbr_data_list = list(zip(pbr_data.columns[1:], pbr_data_list))
        
        # 크롤링 데이터 리스트로 변환
        pbr_data = df.loc[df['주요재무정보'] == 'PBR(배)']
        pbr_data_list = dataframe_to_list(pbr_data)
        
        roe_data = df.loc[df['주요재무정보'] == 'ROE(지배주주)']
        roe_data_list = dataframe_to_list(roe_data)
        
        per_data = df.loc[df['주요재무정보'] == 'PER(배)']
        per_data_list = dataframe_to_list(per_data)
        
        dividend_yield_data = df.loc[df['주요재무정보'] == '시가배당률(%)']
        dividend_yield_list = dataframe_to_list(dividend_yield_data)
        
        dividend_propensity_data = df.loc[df['주요재무정보'] == '배당성향(%)']
        dividend_propensity_list = dataframe_to_list(dividend_propensity_data)
        
        debt_ratio_data = df.loc[df['주요재무정보'] == '부채비율']
        debt_ratio_list = dataframe_to_list(debt_ratio_data)
        
        #for pbr, roe, per, div_y, div_p, debt_r in zip(pbr_data[:5], roe[:5], per_data[:5], dividend_yield_data[:5], dividend_propensity_data[:5], debt_ratio_data[:5]):
        financial_data = FinancialData(pbr_data_list, roe_data_list, per_data_list, dividend_yield_list, dividend_propensity_list, debt_ratio_list)
        stock_year_data, stock_quarter_data = financial_data.data_preprocessing()
        stock_year_data_dict[_code] = stock_year_data
        stock_quarter_data_dict[_code] = stock_quarter_data
    
    return stock_list, stock_year_data_dict, stock_quarter_data_dict
