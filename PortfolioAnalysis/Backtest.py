import pandas as pd
import numpy as np

class Backtest:
    """
    Des: Backtest using historal data and transcation view
    
    Input:
        NA is not allowed
        Monthly frequence
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
        
        ###  Calculate for Net Value of Asset with the transcation views  ###
        ###  Main Idea: use the return return of 2 adjacent days to solve this problem  ###
        
        # price obtained by simply view times history price
        ay_view = np.array(df_view)
        ay_history = np.array(df_history)
        df_price_each = pd.DataFrame(ay_view*ay_history)
        df_price = df_price_each.sum(axis=1)

        # bool value that wether the view changes or not 
        df_view_cg = ((abs(df_view-df_view.shift(1))).sum(axis=1))!=0
        ay_view_cg = np.array(df_view_cg)

        # the price of asset when position changes
        ay_view_close = np.array(df_view.shift(1))*np.repeat(ay_view_cg,3).reshape(6,3) + np.array(df_view.shift(0))*np.repeat(ay_view_cg==0,3).reshape(6,3)
        df_price_each_close = pd.DataFrame(ay_view_close*ay_history)
        df_price_each_close.iloc[0,:] = df_price_each.iloc[0,:]
        ay_price_each_close = np.array(df_price_each_close)

        # the return rate of each day puls 1
        # return between 2 adjacent days = the price of asset when position changes - the price obtained by simply view times history price
        df_r = ((df_price_each_close-df_price_each.shift(1)).sum(axis=1))/df_price.shift(1) + 1
        df_r[0] = 1

        # the true value of assets each month
        df_asset = df_r.cumprod()*100

        # time series of net value with initital asset = initial_asset
        self.df_asset = df_asset
        
        # log return of asserts each month
        df_log_return = (np.log(df_asset)-df_asset.shift(1))/df_asset.shift(1)
        
        self.df_log_return = df_log_return

    # Maximum retracement of the portfolio
    def maxdown(self):
        df_asset = self.df_asset
        md = ((df_asset.cummax()-df_asset)/df_asset).max()
        return md
    
    # Annualized return of the portfolio
    def annualized_return(self):
        YR = self.df_log_return
        return YR*12
    
    # Annualized volatility of the portfolio
    def annualized_volatility(self):
        df_log_return  = self.df_log_return 
        YV = np.std(df_log_return) * np.sqrt(12)
        return YV
    
    # Sharpe ratio of the portfolio
    def sharpe(self):
        ER = self.df_log_return
        RF = self.df_rf
        YV = np.std(self.df_log_return) * np.sqrt(12)
        return (ER-RF)/YV
    
    # Net value of the portfolio
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
        
    