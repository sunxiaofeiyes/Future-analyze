# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 11:06:03 2020

@author: sunxi
"""

'''
计算指标信号的函数
'''
import pandas as pd
import numpy as np
import cal_functions as cf
#df参数是行情数据dataframe，默认0列为时间，1列为开盘价，2列为最高价，3列为最低价，4列为收盘价。,5列为涨跌。
#disrtmoney为初始资金量
#holdday为单次交易的持仓周期
#symbol为交易信号
#per_point为每点变动价格单位，如甲醇每点变动为10元。
symboldit = {'1':'4日均线上穿9日均线',\
             '2':'4日均线上穿18日均线',\
             '3':'9日均线上穿18日均线',\
             '4':'4日均线同时上穿9日、18日均线',\
             '5':'4日均线下破9日均线',\
             '6':'4日均线下破18日均线',\
             '7':'9日均线下破18日均线',\
             '8':'4日均线同时下破9、18日均线',\
             '9':'一阳穿3线',\
             '10':'一阴穿3线',\
             '11':'短期高点形态',\
             '12':'短期低点形态',\
             
        }
def cal_long_win(df,key,firstmoney,symbolindex,holdday,per_point,fees):
    ma4 = cf.calma(df.iloc[:,4],4)
    ma9 = cf.calma(df.iloc[:,4],9)
    ma18 = cf.calma(df.iloc[:,4],18)
    money = firstmoney               #初期资金
    t = len(df.index)           #周期长度
    win = 0                     #盈利次数
    lose = 0                    #亏损次数
    time = 0                    #交易次数
    motwin = []                   #持仓周期出现的最大盈利集合
    motlose = []                  #持仓周期内出现的最大回撤集合
    changes = []                  #价格变动列表
    if key == 'long':
        for i in range(1,t-holdday-1):
            symbol = { '1':ma4[i-1]<ma9[i] and ma4[i]>=ma9[i],\
                  '2':ma4[i-1]<ma18[i-1] and ma4[i]>=ma18[i],\
                  '3':ma9[i-1]<ma18[i-1] and ma9[i]>=ma18[i],\
                  '4':ma4[i-1]<ma9[i-1] and ma4[i-1]<ma18[i-1] and ma4[i]>=ma9[i] and ma4[i]>=ma18[i],\
                  '9':df.iloc[i,1]<ma4[i] and df.iloc[i,1]<ma9[i] and df.iloc[i,1]<ma18[i] and df.iloc[i,4]>ma4[i] and df.iloc[i,4]>ma9[i] and df.iloc[i,4]>ma18[i],\
                  
            }
            
            if symbol[symbolindex]:
                #如果出现交易信号，则交易，交易次数+1
                time += 1
                #开仓价格
                buyprice = df.iloc[i+1,1]
                #平仓价格
                soldprice = df.iloc[i+holdday,4]
                #价格变动 = (卖出价-开盘价)*每点变动价格，甲醇每点为10元，故乘以10
                change = (soldprice-buyprice)*per_point
                changes.append(change)
                #一次交易后资金的变化=资金+盈亏-手续费，手续费默认为1手，甲醇一手默认为20元。
                money += change-fees
                #做多持仓内最大盈利=持仓周期内最高点（最低点）-开仓价
                motwin.append((max(df.iloc[i+1:i+holdday+1,2])-buyprice)*per_point)
                #做多持仓内最大回撤=周期内最低点（最高点）-开仓价
                motlose.append((min(df.iloc[i+1:i+holdday+1,3])-buyprice)*per_point)
                #如果盈利，则win+1，否则lose+1
                if change>0:
                    win += 1
                else:
                    lose += 1
        #t = '初始资金%d元，品种：甲醇主力，利用指标：%s 做多，持仓周期%d天,交易情况如下:\n最终资金为%d元。\n获利次数为%d次。\n亏损次数为%d次。\n交易次数一共%d次。\n持仓内平均最大盈利为%f元。\n持仓内出现的最大盈利为%d元。\n持仓内平均最大亏损为%f元。\n持仓内最大回撤为%d元。\n交易平均盈亏为%f元。\n平均胜率为%f。\n所有交易中最大盈利为%d元。\n所有交易中最大亏损为%d元.'%(firstmoney,symboldit[symbolindex],holdday,money,win,lose,time,np.mean(motwin),max(motwin),np.mean(motlose),min(motlose),np.mean(changes),(win/time)*100,max(changes),min(changes))
        t = {'初始资金':firstmoney,'品种':'甲醇主力','交易方向':'做多','交易指标':symboldit[symbolindex],'持仓周期':holdday,'最终资金':money,'交易次数':time,'获利次数':win,'亏损次数':lose,'胜率':(win/time)*100,'平均盈利':np.mean(changes),'单次交易最大盈利':max(changes),'单次交易最大亏损':min(changes),'持仓内最大盈利':max(motwin),'持仓内最大回撤':min(motlose)}
        t = pd.DataFrame(t,index=[0])
        return t
    if key == 'short':
        for i in range(1,t-holdday-1):
            symbol = { '5':ma4[i-1]>ma9[i] and ma4[i]<=ma9[i],\
                  '6':ma4[i-1]>ma18[i-1] and ma4[i]<=ma18[i],\
                  '7':ma9[i-1]>ma18[i-1] and ma9[i]<=ma18[i],\
                  '8':ma4[i-1]>ma9[i-1] and ma4[i-1]>ma18[i-1] and ma4[i]<=ma9[i] and ma4[i]<=ma18[i],\
                  '10':df.iloc[i,1]>ma4[i] and df.iloc[i,1]>ma9[i] and df.iloc[i,1]>ma18[i] and df.iloc[i,4]<ma4[i] and df.iloc[i,4]<ma9[i] and df.iloc[i,4]<ma18[i],\
                  '11':df.iloc[i-1,2]<df.iloc[i,2]<df.iloc[i+1,2] and df.iloc[i-1,3]<df.iloc[i,3]<df.iloc[i+1,3],\
                  
            }
            if symbol[symbolindex]:
                #如果出现交易信号，则交易，交易次数+1
                time += 1
                #开仓价格
                buyprice = df.iloc[i+1,1]
                #平仓价格
                soldprice = df.iloc[i+holdday,4]
                #价格变动 = (卖出价-开盘价)*每点变动价格，甲醇每点为10元，故乘以10
                change = (buyprice-soldprice)*per_point
                changes.append(change)
                #一次交易后资金的变化=资金+盈亏-手续费，手续费默认为1手，甲醇一手默认为20元。
                money += change-fees
                #做多持仓内最大盈利=持仓周期内最高点（最低点）-开仓价
                motlose.append((buyprice-max(df.iloc[i+1:i+holdday+1,2]))*per_point)
                #做多持仓内最大回撤=周期内最低点（最高点）-开仓价
                motwin.append((buyprice-min(df.iloc[i+1:i+holdday+1,3]))*per_point)
                #如果盈利，则win+1，否则lose+1
                if change>0:
                    win += 1
                else:
                    lose += 1
        #t = '初始资金%d元，品种：甲醇主力，利用指标：%s 做空，持仓周期%d天,交易情况如下:\n最终资金为%d元。\n获利次数为%d次。\n亏损次数为%d次。\n交易次数一共%d次。\n持仓内平均最大盈利为%f元。\n持仓内出现的最大盈利为%d元。\n持仓内平均最大亏损为%f元。\n持仓内最大回撤为%d元。\n交易平均盈亏为%f元。\n平均胜率为%f。\n所有交易中最大盈利为%d元。\n所有交易中最大亏损为%d元.'%(firstmoney,symboldit[symbolindex],holdday,money,win,lose,time,np.mean(motwin),max(motwin),np.mean(motlose),min(motlose),np.mean(changes),(win/time)*100,max(changes),min(changes))
        
        t = {'初始资金':firstmoney,'品种':'甲醇主力','交易方向':'做空','交易指标':symboldit[symbolindex],'持仓周期':holdday,'最终资金':money,'交易次数':time,'获利次数':win,'亏损次数':lose,'胜率':(win/time)*100,'平均盈利':np.mean(changes),'单次交易最大盈利':max(changes),'单次交易最大亏损':min(changes),'持仓内最大盈利':max(motwin),'持仓内最大回撤':min(motlose)}
        t = pd.DataFrame(t,index=[0])
        return t