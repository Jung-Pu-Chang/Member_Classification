import datetime
import numpy as np
import pandas as pd
from pandas import DataFrame
import warnings
warnings.filterwarnings('ignore')

class MemberClass:
    memberID: str
    date: str
    quantity: str
    spend: str
    data: DataFrame
    df: DataFrame
    first_consumption: DataFrame
    last_consumption: DataFrame

    def __init__(self, data, memberID, date, quantity, spend):
        self.memberID = memberID
        self.date = date
        self.quantity = quantity
        self.spend = spend    
        self.data = data[[self.memberID,self.date,self.quantity,self.spend]] 
        
        try :
            self.data[self.memberID] = self.data[self.memberID].astype(str)
        except :
            print('Chk: memberID column contains nan or not')
        
        for fmt in ('%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y', '%d/%m/%Y'):
            try :
                self.data[self.date] = pd.to_datetime(self.data[self.date], format = fmt)
                #print(f"date format is {fmt}")
            except :
                print(f'{fmt} not date format')

        try :
            self.data[self.quantity] = self.data[self.quantity].astype(int)
        except :
            print('Chk: quantity column contains nan、str or not')
          
        try :
            self.data[self.spend] = self.data[self.spend].astype(float)
        except :
            print('Chk: spend column contains nan、str or not')
        
        self.df = self.data.sort_values([self.date, self.memberID], ascending=[True, True])
        self.first_consumption = self.df.drop_duplicates(subset=[self.memberID],keep='first')[[self.date, self.memberID]]
        self.last_consumption = self.df.drop_duplicates(subset=[self.memberID],keep='last')[[self.date, self.memberID]]
        print("All Chk Finished !\nChoosing Caculate Index : LRFM、NES、CAI")
     
    def LRFM(self, year, month, day):
        L = pd.merge(self.first_consumption, self.last_consumption, on=self.memberID,how='inner')
        L['L_raw_days'] = (L[self.date + '_y'] - L[self.date + '_x']).dt.days
        L.loc[(L['L_raw_days'] >= L['L_raw_days'].mean()), "L"] = 1 #高好>>接觸時間長
        self.last_consumption['now'] = pd.to_datetime(datetime.date(year, month, day), format='%Y-%m-%d')
        self.last_consumption['R_raw_days'] = (self.last_consumption['now'] - self.last_consumption[self.date]).dt.days    
        self.last_consumption.loc[(self.last_consumption['R_raw_days'] < self.last_consumption['R_raw_days'].mean()), "R"] = 1 #低好
        self.last_consumption['R'] = self.last_consumption['R'].fillna(0) 
        R = self.last_consumption[[self.memberID,'R_raw_days','R']]
        F = self.df.drop_duplicates(subset=[self.date, self.memberID],keep='first')
        F = F.groupby([self.memberID])[self.quantity].count().reset_index()
        F.loc[(F[self.quantity] >= F[self.quantity].mean()), "F"] = 1
        M = self.df.groupby([self.memberID])[self.spend].sum().reset_index()
        M.loc[(M[self.spend] >= M[self.spend].mean()), "M"] = 1
        LRFM = pd.merge(L[[self.memberID,'L_raw_days','L']], R, on=self.memberID,how='inner')
        LRFM = pd.merge(LRFM, F, on=self.memberID,how='inner')
        LRFM = pd.merge(LRFM, M, on=self.memberID,how='inner')
        LRFM[['L','R','F','M']] = LRFM[['L','R','F','M']].fillna(0) 
        LRFM['LRFM_score_sum'] = LRFM['L'] + LRFM['R'] + LRFM['F'] + LRFM['M']
        print("LRFM index: 1/0 = good/bad")
        return LRFM
    
    def NES(self, year, month, day, period_days, new_def):
        self.last_consumption['now'] = pd.to_datetime(datetime.date(year, month, day), format='%Y-%m-%d')
        self.last_consumption['R_raw_days'] = (self.last_consumption['now'] - self.last_consumption[self.date]).dt.days    
        F = self.df.drop_duplicates(subset=[self.date, self.memberID],keep='first')
        F = F.groupby([self.memberID])[self.quantity].count().reset_index()
        RF = pd.merge(self.last_consumption[[self.memberID,'R_raw_days']], F, on=self.memberID,how='inner')
        RF['freq'] = period_days/RF[self.quantity] # <1 一天多張發票
        RF['freq_ratio'] = RF['R_raw_days']/RF['freq']
        conditions = [(RF['R_raw_days'] < new_def),
                      (RF['freq_ratio'] <= 2), #(RF['freq_ratio'] > 1)&(RF['freq_ratio'] <= 2)
                      (RF['freq_ratio'] > 2)&(RF['freq_ratio'] <= 2.5),
                      (RF['freq_ratio'] > 2.5)&(RF['freq_ratio'] <= 3),(RF['freq_ratio'] > 3)]
        values = ['N', 'E', 'S1', 'S2', 'S3']
        RF['NES'] = np.select(conditions, values)
        return RF
    
    def CAI(self):
        CAI = self.df.drop_duplicates(subset=[self.date, self.memberID],keep='first')
        CAI['weight'] = CAI.groupby([self.memberID]).cumcount() + 1
        CAI['key_n1'] = CAI['weight'] - 1
        CAI['key'] = CAI['weight'].astype(str) + '_' + CAI[self.memberID].astype(str)
        CAI_n1 = CAI[['key_n1',self.memberID,self.date]]
        CAI_n1['key'] = CAI_n1['key_n1'].astype(str) + '_' + CAI_n1[self.memberID].astype(str)
        CAI = pd.merge(CAI[['key',self.memberID,self.date,'weight']], CAI_n1[['key',self.date]], on="key",how='inner')
        CAI['avg_freq'] = (CAI[self.date + '_y'] - CAI[self.date + '_x']).dt.days
        CAI['w_avg_freq'] = CAI['avg_freq'] * CAI['weight']
        CAI_w = CAI.groupby([self.memberID])['w_avg_freq','weight'].sum().reset_index()
        CAI_w['w_avg_freq'] = CAI_w['w_avg_freq']/CAI_w['weight']
        CAI = CAI.groupby([self.memberID])['avg_freq'].mean().reset_index()
        CAI = pd.merge(CAI, CAI_w, on=self.memberID,how='inner')
        CAI['CAI'] = (CAI['avg_freq'] - CAI['w_avg_freq'])/CAI['avg_freq']
        return CAI

if __name__=='__main__': #測試
    path = 'C:/Users/user/Desktop/mastertalk/課程內容/資料集/'
    df = pd.read_csv(path + 'scanner_data.csv', encoding='utf-8',header=0)
    cols = df.columns 

    'init test'
    test = MemberClass(data = df, memberID = cols[2], date = cols[1], quantity = cols[6], spend = cols[7]) 
    LRFM = test.LRFM(2017,1,1)
    NES = test.NES(2017,1,1,366,60)
    CAI = test.CAI()



