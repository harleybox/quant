#!/usr/bin/env python
# encoding: utf-8
"""
@author: Harley
@software: pycharm
@file: stock.PY
@time: 2021/11/5 11:07
@desc:
"""

from jqdatasdk import *
import pandas as pd
import os
import datetime

auth('13922506951', 'Silkroad810')
pd.set_option('display.max_rows', 50000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 2000)

FILE_DIR = '../data/'


def init_db():
    # 获取所有股票代码
    stocks = get_list()
    # 存储到CSV文件中
    for code in stocks:
        df = get_single_price(code)
        export_data(df, filename=code, data_type="price")


def get_list():
    """
    获取所有A股股票列表
    深圳证券交易所  .XSHE  '000001.XSHE' 平安银行
    上海证券交易所  .XSHG  '600519.XSHG' 贵州茅台
    :return: stock_list
    """
    # 将所有股票列表转换成数组
    stock_list = list(get_all_securities(['stock']).index)
    return stock_list


def get_single_price(stock_code, start_date=None, end_date=None, freq='daily'):
    """
    获取单个股票行情数据
    :param stock_code:
    :param start_date:
    :param end_date:
    :param freq:
    :return:
    """

    # 如果start_date=None,默认为从上市日期开始
    if start_date is None:
        start_date = get_security_info(stock_code).start_date
    if end_date is None:
        end_date = datetime.datetime.today()
    # print(start_date)
    # exit()
    # 获取行情数据
    data = get_price(
        stock_code, start_date=start_date, end_date=end_date, frequency=freq,
    )
    return data


def get_index_list(index_symbol='000300.XSHG'):
    """
    获取指数成分股，指数代码查询 https://www.joinquant.com/indexData
    :param index_symbol: 指数的代码
    :return: list,成分股的代码
    """
    stocks = get_index_stocks(index_symbol)
    return stocks


def export_data(data, filename, data_type, mode='w'):
    """
    导出股票行情数据
    :param data:
    :param filename:
    :param data_type: 股票数据类型，可以是：price, finance
    :param mode: w 或 a
    :return:
    """
    file_name = FILE_DIR + data_type + '/' + filename + '.csv'
    data.index.names = ['date']  # 设定header里面的index的名字
    if mode == 'a':
        data.to_csv(file_name, mode=mode, header=False)
        # 删除重复值
        data = pd.read_csv(file_name)
        data = data.drop_duplicates(subset=['date'])  # 以日期作为去重条件
        # data.index.names = ['date']  # 设定header里面的index的名字
        data.to_csv(file_name, index=False)
        print('已成功追加至：', file_name)
    else:
        data.to_csv(file_name)
        print('已成功存储至：', file_name)


def transfer_price_freq(data, time_freq):
    """
    将数据转换为指定周期：开盘价（周期第一天）、收盘价（周期最后一天）、最高价（周期内）、最低价（周期内）
    :param data:
    :param time_freq:
    :return:
    """
    df_trans = pd.DataFrame()
    df_trans['open'] = data['open'].resample(time_freq).first()
    df_trans['close'] = data['close'].resample(time_freq).last()
    df_trans['high'] = data['high'].resample(time_freq).max()
    df_trans['low'] = data['low'].resample(time_freq).min()
    return df_trans


def get_single_finance(code, date, stat_date):
    """
    获取单个股票财务指标
    :param code:
    :param date:
    :param stat_date:
    :return:
    """
    data = get_fundamentals(query(indicator).filter(indicator.code == code), date=date, statDate=stat_date)  # 获取全部财务指标
    return data


def get_single_valuation(code, date, stat_date):
    """
    获取单个股票估值指标
    :param code:
    :param date:
    :param stat_date:
    :return:
    """
    data = get_fundamentals(query(valuation).filter(indicator.code == code), date=date, statDate=stat_date)  # 获取全部财务指标
    return data


def get_csv_data(code, data_type):
    """
    读取csv文件内容
    :param code: filename
    :param data_type: price或者data数据
    :return:
    """
    file_name = FILE_DIR + data_type + '/' + code + '.csv'
    return pd.read_csv(file_name)


def get_csv_price(code, start_date, end_date, data_type='price', columns=None):
    """
    获取本地的数据，且顺便完成数据更新
    :param code: str,股票代码
    :param start_date: str,开始日期
    :param end_date: str, 结束日期
    :param data_type: str,数据类型
    :param columns: list, 选取的字段列
    :return: dataframe
    """
    # 使用update直接更新
    update_daily_price(stock_code=code, data_type='price')
    # 读取数据
    file_name = FILE_DIR + data_type + '/' + code + '.csv'
    # data = pd.read_csv(file_name, index_col='date')
    if columns is None:
        data = pd.read_csv(file_name, index_col='date')
    else:
        data = pd.read_csv(file_name, usecols=columns, index_col='date')
    # print(start_date)
    # print(end_date)
    # # exit()
    # 根据日期筛选股票数据
    return data[(data.index >= start_date) & (data.index <= end_date)]
    # return data[start_date:end_date]


def calculate_change_pct(data):
    """
    涨跌幅 = （当期收盘价 - 前期收盘价） / 前期收盘价
    :param data: dataframe, 带有收盘价
    :return: dataframe 带有涨跌幅
    """
    data['close_pct'] = (data['close'] - data['close'].shift(1)) / data['close'].shift(1)
    return data


def update_daily_price(stock_code, data_type):
    # 3. 每日更新数据
    # 3.1 是否存在文件：不存在-重新获取，存在-> 3.2
    file_name = FILE_DIR + data_type + '/' + stock_code + '.csv'
    if os.path.exists(file_name):
        # 3.2 获取增量数据(code, start_date-数据最后的日期, end_date-今天）
        start_date = pd.read_csv(file_name, usecols=['date'])['date'].iloc[-1]  # date里面的最后一行的数据
        # print(start_date)
        # exit()
        df = get_single_price(stock_code, start_date=start_date, end_date=datetime.datetime.today(), freq='daily')
        # 3.3 追加到已有文件中
        export_data(df, filename=stock_code, data_type=data_type, mode='a')
    else:
        # 重新获取该股票的行情数据
        df = get_single_price(stock_code=stock_code, start_date=None, end_date=datetime.datetime.today(), freq='daily')
        export_data(df, filename=stock_code, data_type=data_type)


if __name__ == '__main__':
    print(len(get_index_list()))
