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
    
    
    def annualized_return(self):
        
    
    def annualized_volatility(self):
        
        
    def shape(self):
        
    
    def net_value(self):
        
        

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
        
    