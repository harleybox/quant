#!/usr/bin/env python
# encoding: utf-8
"""
@author: Harley
@software: pycharm
@file: stock_update_db.py
@time: 2021/11/16 16:46
@desc:
"""
import data.stock as st

# 初始化变量
# code = '000001.XSHG'

# 调用一只股票的行情数据
# data = st.get_single_price(stock_code=code, start_date='2021-02-01', end_date='2021-03-01', freq='daily')

# 存入csv
# st.export_data(data=data, filename=code, data_type='price')

# 实时更新数据: 假设每天更新日K数据 》 存入到csv文件里面 》 data.to_csv(append)

# 1. 获取所有股票代码
stocks = st.get_list()
# 2. 初始化存储到csv文件中
st.init_db()
# 3. 每日更新数据
# for code in stocks:
#     st.update_daily_price(stock_code=code, data_type='price')
