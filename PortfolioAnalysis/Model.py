import pandas as pd
import numpy as np
from scipy.optimize import minimize
from numpy.linalg import inv

class RPModel:
    """
    Des: Risk-Parity Model
    
    Input:
        NA is not allowed
        Monthly frequence
        date(increasing): %Y-%m-%d
        index data: time series of history price of the assets
    """
    

    def __init__(self, df_date, df_index):
        self.df_date = df_date
        self.df_index = df_index
        self.num = self.df_index.shape[1]
        self.r_index = np.log(self.df_index/self.df_index.shift(1))
        
    
    def optimize(self, output = True):
        """
        retur the weights of portfolio after optimization
        """
        
        def Error_Min(w):
            # calculate Total Risk Contribution
            cov_index_p=np.array([],dtype="float64")
            r_p = (self.r_index*w).sum(axis=1)
            sigma_p = r_p.std()
            for i in range(self.num):
                cov_index_p = np.append(cov_index_p, np.cov(self.r_index.iloc[1:,i], r_p[1:])[0, 1])
            mrc = cov_index_p/sigma_p
            trc = w*mrc

            # calculate the deviation
            trc_m = np.array([trc]*self.num)
            trc_m_t = trc_m.T
            e = (trc_m-trc_m_t)**2
            return e.sum()
        
        a = "{'type': 'eq', 'fun': lambda w: w.sum() - 1 }"
        for i in range(self.num):
            a = a + ",{'type': 'ineq', 'fun': lambda w: 1 - w["+str(i)+"] }" + \
            ",{'type': 'ineq', 'fun': lambda w: w["+str(i)+"] + 0.2}"
    
        cons = (eval(a))
        w = [1/self.num,]*self.num
        
        # optimization
        res = minimize(Error_Min,w,constraints=cons,tol = 1e-8)
        
        # output
        if output:
            print("Status: "+str(res.message))
        
        return res.x


class BLModel:
    '''
    Black-Litterman is used to get the final combination weight
    Input:
    
    
    
    '''
    
    def __init__(self, df_date, df_history, df_fr, market_view, sub_view, Q,tau=1, LC=np.array([[0.8]])):
        self.df_date = df_date
        self.df_history = df_history
        self.df_fr = df_fr
        self.num = self.df_history.shape[1]
        self.Q = Q

        self.market_view = np.array(market_view)
        self.sub_view = np.array(sub_view)        
        
        # 风险厌恶系数
        df_r = np.log(df_history/df_history.shift(1)).dropna()
        market_r = (self.market_view*np.array(df_r))
        E_r = market_r.sum(axis = 1).sum(axis = 0)
        mean_fr = df_fr.mean()
        market_sigma = np.std(market_r.sum(axis=1))
        Lambda = ((E_r-mean_fr)/(market_sigma))[0]
        self.Lambda = Lambda
        
        
        
        # 先验收益率（n*1） = Lambda*协方差矩阵（n*n）*权重（n*1）
        market_cov = np.array(df_r.corr())
        Prod = Lambda * np.dot(market_cov , market_view.T)
        self.Prod = Prod
        
        
        # 观点误差矩阵
        P = (sub_view.sum(axis=0))
        CF = np.dot(np.dot(P,market_cov),P.T)
        Omega = CF/LC
        self.Omega = Omega

        
        # 后验收益率 E(R)
        E_R = np.dot(np.linalg.inv(inv(tau*market_cov)+\
                                   np.dot(np.dot(sub_view.T,inv(Omega)),sub_view)),
                         np.dot(inv(tau*market_cov),Prod)+\
                              np.dot(np.dot(sub_view.T,inv(Omega)),Q))
        self.E_R = E_R
        
        # BL协方差矩阵
        Cov_BL = inv(inv(tau*market_cov)+np.dot(np.dot(sub_view.T,inv(Omega)),sub_view))
        self.Cov_BL = Cov_BL
    
    def optimize(self, output=True):
        
        def utility(w):
            u = (w.T.dot(self.E_R)-(self.Lambda/2)*np.dot(w.T,self.Cov_BL).dot(w))
            return -u
        
        
        w = np.array([1/self.num,]*self.num)
        
        a = "{'type': 'eq', 'fun': lambda w: w.sum() - 1 }"
        for i in range(self.num):
            a = a + ",{'type': 'ineq', 'fun': lambda w: 1 - w["+str(i)+"] }" + \
            ",{'type': 'ineq', 'fun': lambda w: w["+str(i)+"] + 0.2}"
    
        cons = (eval(a))
        
        # optimization
        res = minimize(utility,w,constraints=cons,tol = 1e-10)
        
        # output
        if output:
            print("Status: "+str(res.message))
        return res.x
        
        