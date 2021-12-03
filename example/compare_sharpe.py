#!/usr/bin/env python
# encoding: utf-8
"""
@author: Harley
@software: pycharm
@file: compare_sharpe.py
@time: 2021/11/15 17:20
@desc:
"""
from data import stock as st
from strategy import base as stb
from strategy import week_strategy as sts
import pandas as pd
import matplotlib.pyplot as plt

# 获取3只股票的数据:比亚迪 宁德时代 隆基
codes = ['002594.XSHE', '300750.XSHE', '601012.XSHG']
ratios = []  # 存数据
daily_closes = pd.DataFrame()  # 存每天的收盘价
# 创建dataframe，存放三只股票的最大回撤，窗口期为252个交易日
max_drawdown = pd.DataFrame()
# 创建dataframe，存放三只股票应用周四买，周一卖的交易策略的累计收益
week_period = pd.DataFrame()
for code in codes:
    data = st.get_single_price(code, start_date='2018-10-1', end_date='2021-1-1', freq='daily')
    # 计算每只股票的夏普比率
    daily_sharpe, annual_sharpe = stb.calculate_sharp(data)  # 函数返回了2个值，每天和每年的sharpe
    profit_change = data['close'].pct_change()
    mean_profit = profit_change.mean()  # 收益率均值
    draw_down = stb.calculate_max_drawdown(data)
    ratios.append([code, annual_sharpe, mean_profit * 100])  # 填充数据,年度sharpe ratio
    # 获取每日收盘价
    daily_closes[code] = data['close']  # 3个column添加到daily_closes,不需要append
    # 获取最大回撤
    max_drawdown[code] = abs(stb.calculate_max_drawdown(data)['max_drawdown'])
    # 计算本只股票应用周四买、周一卖的策略的累计收益
    df = sts.week_period_strategy(code, '2018-10-1', '2021-1-1', 'daily')
    week_period[code] = df['cum_profit']

df = pd.DataFrame(ratios, columns=['code', 'sharpe', 'mean_profit', ], index=codes)
# print(df)
# print(daily_closes)
# print(week_period)

# 可视化3只股票并比较
df.plot.bar(title='Compare Annual Sharpe Ratio/Profit')
plt.xticks(rotation=0)

# 可视化三只股票的每日收盘价
daily_closes.plot(title='Compare Daily Close Price')

# 可视化三只股票的年最大回撤
max_drawdown.plot(title='Compare Annual Max Drawdown')

# 可视化三只股票采用周四买入，周一卖出的策略的累计收益
week_period.plot(title='Compare Sum Profit')

plt.show()
