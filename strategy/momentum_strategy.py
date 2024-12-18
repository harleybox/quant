#!/usr/bin/env python
# encoding: utf-8
"""
@author: Harley
@software: pycharm
@file: momentum_strategy.py
@time: 2021/11/26 16:13
@desc: 动量策略（正向）
"""
import data.stock as st
import pandas as pd
import numpy as np
import strategy.base as base
import matplotlib.pyplot as plt


def get_data(start_date, end_date, use_cols, index_symbol='000300.XSHG'):
    """
    获取股票收盘价数据，并拼接为一个df
    :param start_date: string
    :param end_date: string
    :param use_cols: list
    :param index_symbol: string
    :return data_concat: df 拼接后的数据
    """
    # 获取股票列表代码：沪深300持有个股、创业板、上证
    stocks = st.get_index_list(index_symbol='000300.XSHG')
    # 拼接收盘价的容器
    data_concat = pd.DataFrame()
    # 获取股票数据
    for code in stocks[:5]:
        data = st.get_csv_price(code, start_date, end_date, data_type='price',
                                columns=['date', 'close'])

        # print("=======", code)
        # 拼接多个股票的收盘价：日期  股票A收盘价  股票B收盘价  股票C收盘价 ...
        data.columns = [code]  # 修改了close这个columns的名字为code
        data_concat = pd.concat([data_concat, data], axis=1)
    # 预览股票数据
    # print(data_concat.dropna())
    return data_concat


def momentum(data_concat, shift_n=1, top_n=2):
    """

    :param data_concat: df
    :param shift_n: int,表示业绩统计周期（单位：月）
    :param top_n: int,排前n的数据，最差的n个，或者最好的n个
    :return:
    """
    # 先将data_concat的index由string转成date
    # print(data_concat.index)
    # exit()
    data_concat.index = pd.to_datetime(data_concat.index)
    # 转换时间频率：日=》月
    data_month = data_concat.resample('M').last()
    # 计算过去shift_n个月的收益率 = 期末值/期初值 -1  = （期末 - 期初） / 期初
    # optional: 对数收益率 = log(期末值/期初值）
    shift_return = data_month / data_month.shift(shift_n) - 1
    print(shift_return.head(5))
    # 生成交易信号： 收益率排前n的->赢家组合->买入->1,排最后n个-》输家-》卖出-》1

    buy_signals = get_top_stocks(shift_return, top_n)
    sell_signals = get_top_stocks(-1 * shift_return, top_n)
    signal = buy_signals - sell_signals
    print(signal.head(5))
    # print(buy_signals)
    # print(sell_signals)

    # 计算投资组合收益率
    returns = base.calculate_portfolio_return(shift_return, signal, top_n * 2)
    print(returns)
    
    # 评估策略效果：总收益率、年收益率、最大回撤、夏普比
    base.evaluate_strategy(returns)
    return returns


def get_top_stocks(res, top_n):
    """
    找到前n位的极值，并转换为信号返回
    :param res:df
    :param top_n: int,表示要产生信号的个数
    :return signals: df, 返回0/1数据表
    """
    # 初始化信号容器
    signals = pd.DataFrame(index=res.index, columns=res.columns)
    # 对data的每一行进行遍历，找里面的最大值，并利用bool函数标注0或者1信号
    for index, row in res.iterrows():
        # print(index, row)
        # print(row.isin(row.nlargest(top_n)))  # row里面最大的top_n标为true，否则标为false
        signals.loc[index] = row.isin(row.nlargest(top_n)).astype(np.int)  # 降上面bool转为0或1
    return signals


if __name__ == '__main__':
    # 测试获取沪深300数据
    data = get_data('2020-01-01', '2021-04-04', ['date', 'close'])
    # 测试： 动量策略
    returns = momentum(data)
    returns.plot()
