#!/usr/bin/env python
# encoding: utf-8
"""
@author: Harley
@software: pycharm
@file: stock.PY
@time: 2021/11/5 11:07
@desc:
"""
import time
from jqdatasdk import *
import data.stock as st

# 初始化变量
code = '000005.XSHE'

# 调用一只股票的行情数据
data = st.get_csv_price(code=code, start_date='2021-01-01', end_date='2021-02-01')
print(data)
# p = get_price('000003.XSHE', count=2, end_date='2015-01-30')
# print(p)
# 计算涨跌幅，验证准确性
# st.calculate_change_pct(data)
# print(data)

# 获取周k
# data = st.transfer_price_freq(data, 'w')
# print(data)
# 打印周k的涨跌幅
# st.calculate_change_pct(data)
# print(data)
