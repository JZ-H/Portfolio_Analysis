import pandas as pd
import numpy as np

class Backtest:
    """
    Des: Backtest using historal data and transcation view
    
    Input:
        date(increasing): %Y/%m/%d
        history data: time series of history price of the assets
        transcation view: view of long, short or close a position
        risk-free rate: time series of risk-free rate
        initial_asset(=100): the value of initital asset
    """
    

    def __init__(self, df_date, df_history,df_rf, df_view,initial_asset=100):
        self.df_date = df_date
        self.initial_asset = initial_asset
        self.df_rf = df_rf
        self.df_history = df_history
        self.df_view = df_view
        

    
    def maxdown(self):
        df_asset = self.df_asset
        md = ((df_asset.cummax()-df_asset)/df_asset).max()
        return md
    
    def annualized_return(self):
        YR = self.df_log_return
        return YR*12
    
    def annualized_volatility(self):
        df_log_return  = self.df_log_return 
        YV = np.std(df_log_return) * np.sqrt(12)
        return YV
        
    def sharpe(self):
        ER = self.df_log_return
        RF = self.df_rf
        YV = np.std(self.df_log_return) * np.sqrt(12)
        return (ER-RF)/YV
    
    def net_value(self):
        return self.df_asset

        

    def output_info(self):
        """
        Des: Print the info of the backtest results
        """
        
    def gen_graph(self):
        """
        Des: gen the graph of backtest (using R)
        """
        
        
    def save_graph(self, path):
        """
        Des: Save the graph of backtest
        Input: 
            path: the path for saving graph
        """
        
    
