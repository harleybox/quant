#!/usr/bin/env python
# encoding: utf-8
"""
@author: Harley
@software: pycharm
@file: strategy_test.py.py
@time: 2021/11/22 17:02
@desc: 练习作业
"""
import data.stock as st
import pandas as pd
import strategy.ma_stratagy as ma
import matplotlib.pyplot as plt

# 获取上市时间大于2016-01-01的股票列表
stock_list = st.get_list()[-10:]
lists = []
for i in stock_list:
    start_date = st.get_security_info(i).start_date
    if (start_date.strftime("%Y-%m-%d")) >= '2016-01-01':
        lists.append(i)

# 获取该列表的日K
daily_close = pd.DataFrame()
for code in lists:
    data = st.get_single_price(stock_code=code, start_date='2021-08-01', end_date=None, freq='daily')
    daily_close[code] = data['close']
# daily_close.plot.bar()
print(daily_close)

# 根据ma策略，计算收益率
cum_profit = pd.DataFrame()
for code in lists:
    df = st.get_single_price(stock_code=code, start_date='2020-08-01', end_date=None, freq='daily')
    df = ma.ma_strategy(df, 5, 20)
    print(df)
    cum_profit[code] = df['cum_profit'].reset_index(drop=True)
    df['cum_profit'].plot(label=code, legend=True)
    print(code, '开仓次数：', int(len(df)))
print(cum_profit)
plt.title('Compare of Ma stratagy Profit')
