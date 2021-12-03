#!/usr/bin/env python
# encoding: utf-8
"""
@author: Harley
@software: pycharm
@file: statistical_test.py
@time: 2021/11/23 16:40
@desc:
"""
import data.stock as st
import strategy.ma_stratagy as ma
import matplotlib.pyplot as plt
from scipy import stats


def ttest(data_return):
    """

    :param data_return: dataframe 单次收益率
    :return: p: float,
    """

    # 调用假设检验ttest函数 ： scipy
    t, p = stats.ttest_1samp(data_return, 0, nan_policy='omit')
    # 获取t,p

    # 判断是否与理论均值有显著差异: a = 0.05
    p_value = p / 2  # 获取单边p值
    print('t-value:', t)
    print('p-value:', p_value)  # 小于0.05，策略似乎更可靠
    print("是否可以拒绝[H0]：收益均值 = 0：", p < 0.05)
    return t, p_value


if __name__ == '__main__':
    # 策略的单次收益率
    stocks = ['000001.XSHE', '000858.XSHE', '002594.XSHE']
    for code in stocks:
        print(code)
        df = st.get_single_price(code, start_date='2016-12-01', end_date='2021-01-01', freq='daily')
        df = ma.ma_strategy(df, 5, 20)
        # 策略的单次收益率
        returns = df['profit_pct']
        # print(returns)
        # 绘制一下分布图用于观察
        # plt.hist(returns)
        # plt.show()
        # 对多个股票进行计算、测试
        ttest(returns)
