#!/usr/bin/env python
# encoding: utf-8
"""
@author: Harley
@software: pycharm
@file: compare_profit.py
@time: 2021/11/12 16:57
@desc:
"""

from strategy import week_strategy
import pandas as pd
import matplotlib.pylab as plt

stock_code = ['000001.XSHE', '600519.XSHG', '000651.XSHE']
df_cum_profit = pd.DataFrame()
for code in stock_code:
    df = week_strategy.week_period_strategy(code, None, '2021-3-1', 'daily', )
    df_cum_profit[code] = df['cum_profit']

print(df_cum_profit)
print(df_cum_profit.describe())
df_cum_profit.plot()
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.title('周期策略下(周四买入周一卖出)三支股票的累计收益率')
plt.show()
