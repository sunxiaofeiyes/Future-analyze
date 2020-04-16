# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 20:54:13 2020

@author: sunxi
"""

import pandas as pd
import numpy as np
import calwin_func as calfunc
#读取本地文件
df = pd.read_csv('C:\\Users\\sunxi\\Pictures\\files\\MA.csv',encoding='gbk')
objs=[]
for keys in ['long','short']:
    if keys == 'long':
        for sym in [1,2,3,4,9]:
            for day in [1,2,3,5,7,10]:
                data = calfunc.cal_long_win(df,key=keys,firstmoney=4000,symbolindex=str(sym),holdday=day,per_point=10,fees=20)
                objs.append(data)
    else:
        for sym in [5,6,7,8,10]:
            for day in [1,2,3,5,7,10]:
                data = calfunc.cal_long_win(df,key=keys,firstmoney=4000,symbolindex=str(sym),holdday=day,per_point=10,fees=20)
                objs.append(data)
ans = pd.concat(objs,axis=0)
ans.to_csv('MA Answer.csv',encoding='utf_8_sig',index=False)
        