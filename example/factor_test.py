#!/usr/bin/env python
# encoding: utf-8
"""
@author: Harley
@software: pycharm
@file: factor_test.py.py
@time: 2021/11/26 10:43
@desc:
"""
import data.stock as st

factor_data = st.get_factor_values(securities=['000001.XSHE'],
                                   factors=['MAC5', 'MAC10', 'boll_down', 'boll_up'], start_date='2019-01-01',
                                   end_date='2021-01-01')
print('====MAC5')
print(factor_data['MAC5'])
print('====MAC10')
print(factor_data['MAC10'])
print('====boll_up')
print(factor_data['boll_up'])
print('====boll_down')
print(factor_data['boll_down'])
