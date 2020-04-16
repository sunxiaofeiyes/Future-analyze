#!/usr/bin/env python
# coding: utf-8

# In[7]:


#指标计算函数集

import pandas as pd
import sqlalchemy as sqla
import numpy as np

#计算移动平均线，传递收盘价数据和周期t
def calma(data,t):
    ma = data.rolling(t).mean()
    return ma

#计算指数移动平均线，传递收盘价数据和周期t
def calema(data,t):
    ema = data.ewm(span=t).mean()
    return ema

#计算rsi，传递收盘价数据和周期t
def calrsi(data,n):
    deltas = np.diff(data)
    seed = deltas[:n + 1]
    up = seed[seed >= 0].sum() / n
    down = -seed[seed < 0].sum() / n
    rs = up / down
    rsi = np.zeros_like(data)
    rsi[:n] = 100. - 100. / (1. + rs)

    for i in range(n, len(data)):
        delta = deltas[i - 1]  

        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up * (n - 1) + upval) / n
        down = (down * (n - 1) + downval) / n

        rs = up / down
        rsi[i] = 100. - 100. / (1. + rs)

    return rsi

#计算macd，传递收盘价，短期，长期，以及中间常量，如12，26，9
def calmacd(data,nlow,nfast,mid):
    emalow = calema(data,nlow)
    emafast = calema(data,nfast)
    dif = emalow - emafast
    dea = calema(dif,mid)
    return emalow,emafast,dif,dea

#计算布林带，传递收盘价，周期，规范量
def calboll(data,t,p):
    boll = calma(data,t)
    std = data.rolling(t).std()
    upboll = boll + p*std
    downboll = boll - p*std
    return boll,upboll,downboll

def calcci(data,t):
    MD = []
    CCI = []
    MA = calma(data['close'],t)
    MA.fillna(0)
    for i in range(len(data)):
        md = MA[i] - data['close'][i]
        MD.append(md)
    MD = pd.DataFrame(MD)
    mds = calma(MD,t)
    for i in range(len(data)):
        TYP = (data['high'][i]+data['low'][i]+data['close'][i])/3
        cci = (TYP-MA[i])/mds.iloc[i]/0.015
        CCI.append(cci)
    return CCI
        


#mysql函数
#与数据库链接函数
def consql(database):
    db_info = {
        'user': 'root',
        'password': '123',
        'host': 'localhost',
        'port': 3306,  
        'database': database
        }
    db = sqla.create_engine('mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)d/%(database)s?charset=utf8' % db_info,encoding='utf-8')
    return db
#读取表中数据，本函数适合于日线蜡烛图绘制
def readsql(table,db):
    data = pd.read_sql('select trade_date,open,high,low,close,vol from %s order by trade_date'% table,db)
    return data


    

# In[ ]:




