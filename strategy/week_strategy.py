#!/usr/bin/env python
# encoding: utf-8
"""
@author: Harley
@software: pycharm
@file: week_strategy.py
@time: 2021/11/8 11:28
@desc: 用来买入卖出信号
"""
import datetime

import data.stock as st
import numpy as np
import pandas as pd
import matplotlib.pylab as plt


def compose_signal(data):
    """
    # 整合信号
    :param data:
    :return:
    """
    # 去除买入重复部分
    data['buy_signal'] = np.where((data['buy_signal'] == 1) &
                                  (data['buy_signal'].shift(1) == 1), 0, data['buy_signal'])  # 本身是1，而且上面那条也是1的话，
    # # 改为0，否则不变

    # 去除卖出重复部分
    data['sell_signal'] = np.where((data['sell_signal'] == -1) &
                                   (data['sell_signal'].shift(1) == -1), 0, data['sell_signal'])  # 本身是1，而且上面那条也是1的话，
    # 改为0，否则不变

    data['signal'] = data['buy_signal'] + data['sell_signal']  # 合并成一个signal
    return data


def calculate_prof_pct(data):
    """
    # 计算单次收益率：开仓、平仓（开仓的全部股数）
    :param data:
    :return:
    """
    data = data.loc[data['signal'] != 0].copy()  # 先建立副本，否则报错
    data['profit_pct'] = (data['close'] - data['close'].shift(1)) / data['close'].shift(1)  # 筛除没有交易的日期并计算收益率
    data = data[data['signal'] == -1]  # 筛除买入交易的日期
    return data


def calculate_cum_prof(data):
    """
    #计算累计收益率公式：(1+当天收益率）的累计乘积-1
    :param data:
    :return:
    """
    data['cum_profit'] = pd.DataFrame(1 + data['profit_pct']).cumprod() - 1  # (1+当天收益率）的累计乘积-1
    return data


# 计算回撤
def calculate_max_drawdown(data):
    """
    计算最大回车比
    :param data:
    :return:
    """
    # 选取时间周期 （时间窗口）
    window = 252  # 按一年交易日
    # 选取时间周期中的最大净值
    data['rolling_max'] = data['close'].rolling(window=window, min_periods=1).max()
    # 计算当天的回撤比 = （谷值-峰值）/峰值 = 谷值/峰值 -1
    data["daily_drawdown"] = data['close'] / data['rolling_max'] - 1  # 负数
    # 选取时间周期内最大的回撤比，即最大回撤
    data["max_drawdown"] = data["daily_drawdown"].rolling(window, min_periods=1).min()  # 最小值即绝对值更大，回撤就更大
    return data


# 计算夏普比率
def calculate_sharp(data):
    """
    # 计算夏普比率, 返回日或年的夏普比率
    :param data:
    :return: float
    """
    # 公式： sharp = (回报率的均值-无风险利率) / 回报率的偏差 ; 无风险利率几乎为0
    # 因子项
    # #回报率均值 = 日涨跌幅.mean()
    arg_return = data['close'].pct_change().mean()  # pct_change()收盘价涨跌值的平均值
    # #回报率的偏差 = 日涨跌幅.std deviation
    std_return = data['close'].pct_change().std()  # std()收盘价涨跌的标准偏差
    # 计算夏普-按日
    sharpe = arg_return / std_return
    # 计算夏普-按年
    sharp_year = sharpe * np.sqrt(252)
    return sharpe, sharp_year


# 周交易策略
def week_period_strategy(stock_code, start_date, end_date, freq):
    data = st.get_single_price(stock_code, start_date, end_date, freq)
    data['weekday'] = data.index.weekday
    # 周四买入
    data['buy_signal'] = np.where((data['weekday'] == 3), 1, 0)  # 周四的时候操作，满足条件1是买入，不满足条件0是不操作
    # 周一卖出
    data['sell_signal'] = np.where((data['weekday'] == 0), -1, 0)  # 周一的时候操作，满足条件-1是卖出，不满足条件0是不操作

    # 模拟连续重复交易
    # data['sell_signal'] = np.where((data['weekday'] == 1) | (data['weekday'] == 2), -1, 0)  # 周四和周五的时候操作，
    # 满足条件1是买入，不满足条件0是不操作

    data = compose_signal(data)  # 整合信号
    data = calculate_prof_pct(data)  # 计算收益率
    data = calculate_cum_prof(data)  # 计算累计收益率

    return data


if __name__ == '__main__':  # 可以直接从本文件执行以下脚本，避免导入和被执行
    # df = week_period_strategy('000001.XSHE', None, '2021-3-1', 'daily')
    # print(df[['close', 'buy_signal', 'sell_signal', 'signal', 'profit_pct', 'cum_profit']])
    # print(df.describe())
    # df['cum_profit'].plot()
    # plt.show()

    # 计算平安银行的时间周期内的最大回撤
    # df = st.get_single_price('000001.XSHE', None, '2021-3-1', 'daily')
    # df = calculate_max_drawdown(df)
    # print(df[['close', 'rolling_max', 'daily_drawdown', 'max_drawdown']])
    # df[['daily_drawdown', 'max_drawdown']].plot()
    # plt.show()

    # 计算平安银行夏普比率
    df = st.get_single_price('000001.XSHE', None, '2021-3-1', 'daily')
    sharpe = calculate_sharp(df)
    print(sharpe)
