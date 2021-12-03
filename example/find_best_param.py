#!/usr/bin/env python
# encoding: utf-8
"""
@author: Harley
@software: pycharm
@file: find_best_param.py
@time: 2021/11/23 19:55
@desc:寻找最优参数
"""

import strategy.ma_stratagy as ma
import data.stock as st
import pandas as pd

# 参数1： 股票池
data = st.get_csv_price('000001.XSHE', start_date='2016-01-01', end_date='2021-01-01',
                        data_type='price')

# 参数2： 周期参数
params = [5, 10, 20, 60, 120, 250]
# 放入参数和收益
res = []

# 匹配并计算不同的周期参数对
for short in params:
    for long in params:
        if long > short:
            data_res = ma.ma_strategy(data=data, short_window=short, long_window=long)
            # 获取周期参数，及其对应累计收益率
            cum_profit = data_res['cum_profit'].iloc[-1]
            res.append([short, long, cum_profit])

# 将结果转换为df，并找到最优参数
res = pd.DataFrame(res, index=None, columns=['short_win', 'long_win', 'cum_profit'])
res = res.sort_values(by='cum_profit', ascending=False)  # 按照收益倒序排列

print(res)
