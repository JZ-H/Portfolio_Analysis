import pandas as pd
import numpy as np

import time
from datetime import date
from matplotlib import pyplot as plt
import matplotlib.dates as dt

def Plot2(date,data1,data2,title="",label1="",label2="",\
         save_path=False,figure_size=[18,4]):

    year = dt.YearLocator()
    yearformat = dt.DateFormatter('%Y')
    fig=plt.figure(figsize=figure_size)
    ax = fig.add_subplot(1, 1, 1)
    ax.plot_date(pd.to_datetime(date),data1,'-',\
                 linewidth = 2.5,label=label1, alpha=1)
    ax.plot_date(pd.to_datetime(date),data2,'-',\
                 linewidth = 2.5,label=label2, alpha=1)
    ax.xaxis.set_major_locator(year)
    #ax.yaxis.set_major_formatter(FuncFormatter(to_percent))
    ax.xaxis.set_major_formatter(yearformat)
    ax.legend(fontsize=14)
    ax.set_title(title,fontsize=20)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    if save_path:
        fig.savefig(save_path) 
        
def Plot3(date,data1,data2,data3,title="",label1="",\
          label2="",label3="",save_path=False,figure_size=[18,4]):
    """
    Plot with 3 Series
    """
    year = dt.YearLocator()
    yearformat = dt.DateFormatter('%Y')
    fig=plt.figure(figsize=figure_size)
    ax = fig.add_subplot(1, 1, 1)
    ax.plot_date(pd.to_datetime(date),data1,'-',\
                 linewidth = 2.5,label=label1, alpha=1)
    ax.plot_date(pd.to_datetime(date),data2,'-',\
                 linewidth = 2.5,label=label2, alpha=1)
    ax.plot_date(pd.to_datetime(date),data3,'-',\
                 linewidth = 2.5,label=label3, alpha=1)
    ax.xaxis.set_major_locator(year)
    #ax.yaxis.set_major_formatter(FuncFormatter(to_percent))
    ax.xaxis.set_major_formatter(yearformat)
    ax.legend(fontsize=14)
    ax.set_title(title,fontsize=20)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    if save_path:
        fig.savefig(save_path)

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
        freq: M, Q, D, Y
        initial_asset(=100): the value of initital asset
    """
    

    def __init__(self, df_date, df_history, df_view, df_rf,freq,initial_asset=100):
        self.df_date = df_date
        self.initial_asset = initial_asset
        self.df_rf = df_rf
        self.df_history = df_history
        self.df_view = df_view
        self.freq = freq
        if(self.freq == 'Y') :
            self.times = 1
        if(self.freq == 'Q') :
            self.times = 4
        if(self.freq == 'M') :
            self.times = 12
        if(self.freq == 'D') :
            self.times = 252

        ###  Calculate for Net Value of Asset with the transcation views  ###
        
        df_r = np.log(self.df_history/self.df_history.shift(1))
        # price obtained by simply view times history price
        ay_view = np.array(df_view)
        ay_history = np.array(df_history)
        ay_r = np.array(df_r)
        df_r = pd.DataFrame(ay_view*ay_r)
        
        # return of each asset
        self.df_r_all = df_r
        
        df_r = df_r.sum(axis = 1)
        df_r[0] = 0
        df_r = df_r + 1

        # the true value of assets each month
        df_asset = df_r.cumprod()*100

        # time series of net value with initital asset = initial_asset
        self.df_asset = df_asset
        self.df_r = df_r

    # Maximum retracement of the portfolio
    def maxdown(self):
        df_asset = self.df_asset
        md = ((df_asset.cummax()-df_asset)/df_asset).max()
        return md
    
    # Annualized return of the portfolio
    def annualized_return(self):
        Times = self.times
        df_asset = self.df_asset
        start = 0;
        lst_annualized_return = []
        while(True):
            try:
                df_asset[start+Times]
            except:
                break
            if(len(df_asset[start:start+Times+1])<Times):
                break
            Log_return = (df_asset[start+Times-1] - df_asset[start])/df_asset[start]
            lst_annualized_return.append(Log_return)
            start = start + Times
        return (np.array(lst_annualized_return))
    
    # Annualized volatility of the portfolio
    def annualized_volatility(self):
        YV = np.std(self.annualized_return()) * np.sqrt(self.times)
        return YV
    
    # Sharpe ratio of the portfolio
    def sharpe(self):
        ER = self.annualized_return().mean()
        RF = self.df_rf.mean()[0]
        YV = self.annualized_volatility()
        return (ER - RF) / YV
    
    # Net value of the portfolio
    def net_value(self):
        return self.df_asset
        
    def print_info(self):
        """
        Des: Print the info of the backtest results

        """
        printf("The maxdown is %.4f"%(self.maxdown())+"\n")
        printf("The annualized return is %.4f"%(self.annualized_return())+"\n")
        printf("The annualized volatility is %.4f"%(self.annualized_volatility().mean())+"\n")
        printf("The annualized sharpe ratio is %.4f"%(self.sharpe())+"\n")

    def get_info(self):
        SP = self.sharpe()
        YR = self.annualized_return().mean()
        YV = self.annualized_volatility()
        MD = self.maxdown()
        info = pd.DataFrame({"Sharpe":SP,"Annualized Return":YR,"Annualized Volatility":YV,
                            "Maximum Drawdown":MD},index=["Value"])
        return info
        
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
        
    