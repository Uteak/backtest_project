import FinanceDataReader as fdr
from backtesting import Backtest, Strategy
import talib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
import base64
from io import BytesIO

class MyStrategy(Strategy):
    def init(self):
        close_prices = self.data.Close.astype('float64')
        self.ma = self.I(talib.SMA, close_prices, 50)
    
    def next(self):
        if self.data.Close[-1] > self.ma[-1]:
            self.buy()

class BackTestClass():
    company_codes : list
    company_names : list
    start_data : str
    end_date : str
    
    def __init__(self, company_codes, company_names, start, end):
        self.company_codes = company_codes
        self.company_names = company_names
        self.start_data = start + '-01'
        self.end_date = end + '-01'
    
    def accumulate_graph(self):
        image_saves = []
        
        company_codes = self.company_codes
        company_names = self.company_names
        start_date = self.start_data
        end_date = self.end_date
        portfolio_returns = pd.DataFrame(index=pd.date_range(start=start_date, end=end_date))

        # 코스피 지수 데이터 가져오기
        kospi_data = fdr.DataReader('KS11', start=start_date, end=end_date)
        kospi_returns = kospi_data['Close'].pct_change().fillna(0).resample('M').apply(lambda x: (x + 1).cumprod() - 1)

        for code, _name in zip(company_codes, company_names):
            data = fdr.DataReader(code, start=start_date, end=end_date)
            data = data.astype('float64')

            if not data.empty:
                bt = Backtest(data, MyStrategy, cash=100000000, commission=.002)
                results = bt.run()
                equity = results._equity_curve['Equity']
                daily_returns = equity.pct_change().fillna(0)
                portfolio_returns[code] = daily_returns

        portfolio_returns['Total'] = portfolio_returns.mean(axis=1)
        monthly_returns = portfolio_returns.resample('M').apply(lambda x: (x + 1).cumprod() - 1)

        # 전체 포트폴리오의 월별 누적 수익률 그래프 그리기 및 코스피 지수 추가
        plt.figure(figsize=(12, 8))
        monthly_returns['Total'].cumsum().plot(title='Cumulative Monthly Return of Total Portfolio with KOSPI', linewidth=2)
        kospi_returns.cumsum().plot(label='KOSPI Index', style='--', linewidth=2)
        plt.xlabel('Time')
        plt.ylabel('Cumulative Monthly Return')
        plt.legend()
        #plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter())
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)
        
        # Encode the image as base64
        image_png = buffer.getvalue()
        buffer.close()
        image_base64 = base64.b64encode(image_png)
        image_data = image_base64.decode('utf-8')
        return image_data
        # image_saves.append(image_data)

        # # 각 종목별 그래프 그리기 및 코스피 지수 추가
        # for ticker in tickers:
        #     plt.figure(figsize=(12, 8))
        #     monthly_returns[ticker].cumsum().plot(title=f'Cumulative Monthly Returns of {ticker} with KOSPI')
        #     kospi_returns.cumsum().plot(label='KOSPI Index', style='--')
        #     plt.xlabel('Time')
        #     plt.ylabel('Cumulative Monthly Returns')
        #     plt.legend()
        #     buffer = BytesIO()
        #     plt.savefig(buffer, format='png')
        #     plt.close()
        #     buffer.seek(0)

        #     # Encode the image as base64
        #     image_png = buffer.getvalue()
        #     buffer.close()
        #     image_base64 = base64.b64encode(image_png)
        #     image_data = image_base64.decode('utf-8')
        #     image_saves.append(image_data)
        
        # return image_saves

    def return_graph(self):
        image_saves = []
        company_codes = self.company_codes
        company_names = self.company_names
        
        start_date = self.start_data
        end_date = self.end_date
        portfolio_returns = pd.DataFrame()

        for code in company_codes:
            data = fdr.DataReader(code, start=start_date, end=end_date)
            data = data.astype('float64')
            
            if not data.empty:
                bt = Backtest(data, MyStrategy, cash=100000000, commission=.002)
                results = bt.run()
                equity = results._equity_curve['Equity']
                # 월별 수익률 계산
                monthly_returns = equity.resample('M').last().pct_change().fillna(0)
                portfolio_returns[code] = monthly_returns

        # 전체 포트폴리오 수익률 계산
        portfolio_returns['Total'] = portfolio_returns.mean(axis=1)

        # 각 종목별 그래프 그리기
        for code, _name in zip(company_codes, company_names):
            plt.figure(figsize=(12, 8))
            plt.plot(portfolio_returns.index, (portfolio_returns[code].cumsum()) * 100, label=_name, linewidth=2)
            plt.title(f'Cumulative Monthly Returns of {_name}')
            plt.xlabel('Time')
            plt.ylabel('Cumulative Returns (%)')
            plt.legend()
            plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter())
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            buffer.seek(0)

            # Encode the image as base64
            image_png = buffer.getvalue()
            buffer.close()
            image_base64 = base64.b64encode(image_png)
            image_data = image_base64.decode('utf-8')
            image_saves.append(image_data)
            
        # 전체 포트폴리오 그래프 그리기
        plt.figure(figsize=(12, 8))
        plt.plot(portfolio_returns.index, (portfolio_returns['Total'].cumsum()) * 100, label='Total Portfolio', linewidth=2)
        plt.title('Cumulative Monthly Returns of Total Portfolio')
        plt.xlabel('Time')
        plt.ylabel('Cumulative Returns (%)')
        plt.legend()
        plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter())
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)
        # Encode the image as base64
        image_png = buffer.getvalue()
        buffer.close()
        image_base64 = base64.b64encode(image_png)
        image_data = image_base64.decode('utf-8')
        image_saves.append(image_data)
        
        return image_saves
    
    def calculate_metrics(self):
        risk_free_rate = 0.02 / 12  # Adjust this as needed
        results = []

        for code in self.company_codes:
            data = fdr.DataReader(code, start=self.start_data, end=self.end_date)
            data = data.astype('float64')

            if not data.empty:
                bt = Backtest(data, MyStrategy, cash=100000000, commission=.002)
                backtest_results = bt.run()

                equity = backtest_results._equity_curve['Equity']
                monthly_returns = equity.resample('M').last().pct_change().fillna(0)
                cumulative_return = (monthly_returns + 1).cumprod() - 1
                sharpe_ratio = (monthly_returns.mean() - risk_free_rate) / monthly_returns.std()

                results.append({
                    'Code': code,
                    'Average Monthly Return': monthly_returns.mean(),
                    'Cumulative Return': cumulative_return.iloc[-1],
                    'Sharpe Ratio': sharpe_ratio
                })

        return pd.DataFrame(results)
    # def return_graph(self):
    #     image_saves = []
    #     company_codes = self.company_codes
    #     company_names = self.company_names
        
    #     start_date = self.start_data
    #     end_date = self.end_date
    #     portfolio_returns = pd.DataFrame()
    #     for code in company_codes:
    #         data = fdr.DataReader(code, start=start_date, end=end_date)
    #         data = data.astype('float64')
            
    #         if not data.empty:
    #             bt = Backtest(data, MyStrategy, cash=100000000, commission=.002)
    #             results = bt.run()
    #             equity = results._equity_curve['Equity']
    #             # 월별 수익률 계산
    #             monthly_returns = equity.resample('M').last().pct_change().fillna(0)
    #             portfolio_returns[code] = monthly_returns
    #     # 전체 포트폴리오 수익률 계산
    #     portfolio_returns['Total'] = portfolio_returns.mean(axis=1)
    #     # 각 종목별 그래프 그리기
        
    #     for code, _name in zip(company_codes, company_names):
    #         plt.figure(figsize=(12, 8))
    #         plt.plot(portfolio_returns.index, (portfolio_returns[code].cumsum()) * 100, label=_name)
    #         plt.title(f'Cumulative Monthly Returns of {_name}')
    #         plt.xlabel('Time')
    #         plt.ylabel('Cumulative Returns (%)')
    #         buffer = BytesIO()
    #         plt.savefig(buffer, format='png')
    #         plt.close()
    #         buffer.seek(0)

    #         # Encode the image as base64
    #         image_png = buffer.getvalue()
    #         buffer.close()
    #         image_base64 = base64.b64encode(image_png)
    #         image_data = image_base64.decode('utf-8')
    #         image_saves.append(image_data)
            
    #     # 전체 포트폴리오 그래프 그리기
    #     plt.figure(figsize=(12, 8))
    #     plt.plot(portfolio_returns.index, (portfolio_returns['Total'].cumsum()) * 100, label='Total Portfolio', linewidth=1, linestyle='-')
    #     plt.title('Cumulative Monthly Returns of Total Portfolio')
    #     plt.xlabel('Time')
    #     plt.ylabel('Cumulative Returns (%)')
    #     buffer = BytesIO()
    #     plt.savefig(buffer, format='png')
    #     plt.close()
    #     buffer.seek(0)
    #     # Encode the image as base64
    #     image_png = buffer.getvalue()
    #     buffer.close()
    #     image_base64 = base64.b64encode(image_png)
    #     image_data = image_base64.decode('utf-8')
    #     image_saves.append(image_data)
        
    #     return image_saves
    
    
# test = BackTestClass(['005930', '000660', '373220', '207940'], ['삼성전자', 'SK하이닉스', 'LG에너지솔루션', '삼성바이오로직스'], '2018-01', '2023-01')
# test.accumulate_graph()
# test.return_graph()
# result = test.calculate_metrics()
# print(result)
