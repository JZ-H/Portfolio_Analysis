import pandas as pd
import numpy as np
from scipy.optimize import minimize

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
        
        cons = ({'type': 'eq', 'fun': lambda w: w.sum() - 1 })
        w = [1/self.num,]*self.num
        
        # optimization
        res = minimize(Error_Min,w,constraints=cons,tol = 1e-8)
        
        # output
        if output:
            print("Status: "+str(res.message))
        
        return res.x
    