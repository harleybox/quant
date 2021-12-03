#!/usr/bin/env python
# encoding: utf-8
"""
@author: Harley
@software: pycharm
@file: ma_strategy.py
@time: 2021/11/19 16:49
@desc: 双均线策略
"""
import data.stock as st
import pandas as pd
import numpy as np
import strategy.base as strat
import matplotlib.pyplot as plt


def ma_strategy(data, short_window, long_window):
    """
    双均线策略
    :param data: dataframe, 投资标的行情数据，必须包括close
    :param short_window: 短期n日平均线，默认5
    :param long_window: 长期n日平均线，默认20
    :return:
    """
    print("========周期参数为:", short_window, long_window)
    # 计算技术指标： MA短期、MA长期
    data = pd.DataFrame(data)
    data['short_ma'] = data['close'].rolling(window=short_window).mean()
    data['long_ma'] = data['close'].rolling(window=long_window).mean()

    # 生成信号：金叉买入，死叉卖出
    data['buy_signal'] = np.where(data['short_ma'] > data['long_ma'], 1, 0)  # 1是买入
    data['sell_signal'] = np.where(data['short_ma'] < data['long_ma'], -1, 0)  # -1是卖出

    # 过滤信号: st.compose_signal
    data = strat.compose_signal(data)
    # print(data[['close', 'short_ma', 'long_ma', 'buy_signal', 'sell_signal', 'signal']])

    # 计算单次收益
    data = strat.calculate_prof_pct(data)

    # 计算累计收益
    data = strat.calculate_cum_prof(data)

    # 删除多余的列
    # data = data.drop(['buy_signal', 'sell_signal'], axis=1)  # 1表示列
    # data = data[['close', 'short_ma', 'long_ma', 'signal']]
    print(data[['close', 'short_ma', 'long_ma', 'buy_signal', 'sell_signal', 'signal', 'cum_profit']])
    return data


if __name__ == '__main__':
    stocks = ['000001.XSHE', '000858.XSHE', '002594.XSHE']
    cum_profit = pd.DataFrame()
    for code in stocks:
        df = st.get_single_price(code, start_date='2016-01-01', end_date='2021-1-01', freq='daily')
        df = ma_strategy(df, 5, 20)
        # 筛选有信号点
        # df = df[df['signal'] != 0]
        cum_profit[code] = df['cum_profit'].reset_index(drop=True)  # 存储累计收益率, 去掉之前的日期为索引
        # 折线图
        df['cum_profit'].plot(label=code, legend=True)
        # 预览数据
        print(code, '开仓次数：', int(len(df) / 2))
        # print(df[['close', 'short_ma', 'long_ma', 'signal', 'profit_pct', 'cum_profit']])
    print(cum_profit)
    # cum_profit.plot() # 没用日期索引
    plt.title('Compare of Ma strategy Profit')
