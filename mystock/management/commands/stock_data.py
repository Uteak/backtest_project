
class FinancialData():
    pbr_lst : list
    roe_lst : list
    per_lst : list
    divid_y_lst : list
    divid_p_lst : list
    debt_r_lst : list
    
    def __init__(self, pbr_data_list, roe_data_list, per_data_list, dividend_yield_list, dividend_propensity_list, debt_ratio_list):
        self.pbr_lst = pbr_data_list
        self.roe_lst = roe_data_list
        self.per_lst = per_data_list
        self.divid_y_lst = dividend_yield_list
        self.divid_p_lst = dividend_propensity_list
        self.debt_r_lst = debt_ratio_list

    
    def data_preprocessing(self,):
        stock_year_data = []
        stock_quarter_data = []
        
        for data in zip(self.pbr_lst[:4], self.roe_lst[:4], self.per_lst[:4], self.divid_y_lst[:4], self.divid_p_lst[:4], self.debt_r_lst[:4]):
            year = data[0][0]
            pbr = data[0][1]
            roe = data[1][1]
            per = data[2][1]
            dividend_yield = data[3][1]
            dividend_propensity = data[4][1]
            debt_ratio = data[5][1]

            if '(E)' in year:
                year = year.split("(E)")[0]

            stock_year_data.append((year, pbr, roe, per, dividend_yield, dividend_propensity, debt_ratio))
            
        for data in zip(self.pbr_lst[6:], self.roe_lst[6:], self.per_lst[6:], self.divid_y_lst[6:], self.divid_p_lst[6:], self.debt_r_lst[6:]):
            year = data[0][0]
            pbr = data[0][1]
            roe = data[1][1]
            per = data[2][1]
            dividend_yield = data[3][1]
            dividend_propensity = data[4][1]
            debt_ratio = data[5][1]

            if '(E)' in year:
                year = year.split("(E)")[0]

            stock_quarter_data.append((year, pbr, roe, per, dividend_yield, dividend_propensity, debt_ratio))
            
        return stock_year_data, stock_quarter_data