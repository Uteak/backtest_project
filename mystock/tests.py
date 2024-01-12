import FinanceDataReader as fdr
from backtesting import Backtest, Strategy
import talib
import matplotlib.pyplot as plt
import pandas as pd
import base64
from io import BytesIO

class MyStrategy(Strategy):
    def init(self):
        # 데이터 타입을 float64로 변환합니다.
        close_prices = self.data.Close.astype('float64')
        self.ma = self.I(talib.SMA, close_prices, 50)
    
    def next(self):
        if self.data.Close[-1] > self.ma[-1]:
            self.buy()

class BackTestClass():
    stock_list : list
    start_data : str
    end_date : str
    
    def __init__(self, stock_list, start, end):
        self.stock_list = stock_list
        self.start_data = start + '-01'
        self.end_date = end + '-01'
        return
    
    def backtest(self):
        
        #ohlcv = fdr.DataReader(self.stock_list, start=self.start_data, end=self.end_date)
        tickers = self.stock_list
        start_date = self.start_data
        end_date = self.end_date
        portfolio_returns = pd.DataFrame(index=pd.date_range(start=start_date, end=end_date))

        for ticker in tickers:
            data = fdr.DataReader(ticker, start=start_date, end=end_date)
            data = data.astype('float64')

            if not data.empty:
                bt = Backtest(data, MyStrategy, cash=100000000, commission=.002)
                results = bt.run()
                # 각 종목의 일별 수익률 계산
                equity = results._equity_curve['Equity']
                daily_returns = equity.pct_change().fillna(0)
                portfolio_returns[ticker] = daily_returns

        # 각 종목들을 동일한 비율로 투자했을 때의 전체 포트폴리오 수익률 계산
        portfolio_returns['Total'] = portfolio_returns.mean(axis=1)

        # 그래프 그리기
        plt.figure(figsize=(12, 8))
        for ticker in tickers:
           plt.plot(portfolio_returns.index, portfolio_returns[ticker].cumsum(), label=ticker)

        # 전체 포트폴리오 수익률 추가
        plt.plot(portfolio_returns.index, portfolio_returns['Total'].cumsum(), label='Total Portfolio', linewidth=1, linestyle='-')

        plt.title('Cumulative Returns of Individual Stocks and Total Portfolio')
        plt.xlabel('Time')
        plt.ylabel('Cumulative Returns')
        plt.legend()
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)

        # Encode the image as base64
        image_png = buffer.getvalue()
        buffer.close()
        image_base64 = base64.b64encode(image_png)
        image_data = image_base64.decode('utf-8')
        
        #plt.show()
        return image_data


test = BackTestClass(['005930', '000660', '373220', '207940'], '2018-01', '2023-01')
test = test.backtest()

'''     
# 기업 목록
tickers = ['005930', '000660', '373220', '207940']
start_date = '2018-01-01'
end_date = '2023-01-01'

# 각 종목별 수익률 및 전체 포트폴리오 수익률을 계산
portfolio_returns = pd.DataFrame(index=pd.date_range(start=start_date, end=end_date))

for ticker in tickers:
    data = fdr.DataReader(ticker, start=start_date, end=end_date)
    data = data.astype('float64')

    if not data.empty:
        bt = Backtest(data, MyStrategy, cash=10000000, commission=.002)
        results = bt.run()
        # 각 종목의 일별 수익률 계산
        equity = results._equity_curve['Equity']
        daily_returns = equity.pct_change().fillna(0)
        portfolio_returns[ticker] = daily_returns
        
# 각 종목들을 동일한 비율로 투자했을 때의 전체 포트폴리오 수익률 계산
portfolio_returns['Total'] = portfolio_returns.mean(axis=1)

# 그래프 그리기
plt.figure(figsize=(12, 8))
for ticker in tickers:
   plt.plot(portfolio_returns.index, portfolio_returns[ticker].cumsum(), label=ticker)

# 전체 포트폴리오 수익률 추가
plt.plot(portfolio_returns.index, portfolio_returns['Total'].cumsum(), label='Total Portfolio', linewidth=1, linestyle='-')

plt.title('Cumulative Returns of Individual Stocks and Total Portfolio')
plt.xlabel('Time')
plt.ylabel('Cumulative Returns')
plt.legend()
plt.show()
''' 

    
    
'''    
# 삼성전자의 심볼을 사용합니다.
ticker = "005930" 
start_date = "2022-01-01"
end_date = "2023-01-01"

# FinanceDataReader를 사용하여 OHLCV 데이터를 가져옵니다.
ohlcv = fdr.DataReader(ticker, start=start_date, end=end_date)

# 데이터가 제대로 로드되었는지 확인합니다.
print(ohlcv.head())

# 데이터 타입을 float64로 변환합니다.
ohlcv = ohlcv.astype('float64')

# 데이터가 비어있지 않은지 확인합니다.
if not ohlcv.empty:
    # 초기 현금을 늘립니다.
    bt = Backtest(ohlcv, MyStrategy, cash=10000000, commission=.002)
    results = bt.run()

    plt.figure(figsize=(10, 6))
    plt.plot(results._equity_curve['Equity'])
    plt.title('Backtest Result')
    plt.xlabel('Time')
    plt.ylabel('Equity')
    plt.show()
else:
    print("데이터가 비어 있습니다. 티커나 날짜 범위를 확인하세요.")
'''
