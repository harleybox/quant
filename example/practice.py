#!/usr/bin/env python
# encoding: utf-8
"""
@author: Harley
@software: pycharm
@file: practice.PY
@time: 2021/11/5 13:41
@desc:
"""

import data.stock as st
import time

# 初始化变量
# code='000001.XSHG'


start_date = '2021-07-01'
oneday_time = 24 * 60 * 60

# 本章小结：实时更新数据
# 将所有股票列表转换成数组，测试取5条
stock_list = st.get_list()[:5]


def timer():
    # 获取当前日期
    now_date = time.strftime('%Y-%m-%d')  # 2021-11-05
    # 获取当前时间戳
    now_strptime = int(time.time())  # 1636093647
    # 计算今天收盘时间戳
    close_strptime = int(time.mktime(time.strptime(now_date + ' 16:00:00', "%Y-%m-%d %H:%M:%S")))  # 1636099200

    # 计算昨天时间戳
    yesterday_strptime = int(time.mktime(time.strptime(now_date, "%Y-%m-%d"))) - oneday_time  # 1635955200
    # 昨天时间戳转换为日期
    yesterday_date = time.strftime('%Y-%m-%d', time.localtime(yesterday_strptime))  # 2021-11-04

    # 计算明天时间戳
    tomorrow_strptime = int(time.mktime(time.strptime(now_date, "%Y-%m-%d"))) + oneday_time  # 1636128000
    # 明天时间戳转换为日期
    tomorrow_date = time.strftime('%Y-%m-%d', time.localtime(tomorrow_strptime))  # 2021-11-06

    # 获取现在到明天凌晨的秒数
    sleep_time = tomorrow_strptime - now_strptime  # 33893
    # 获取现在到收盘的秒数
    close_time = close_strptime - now_strptime  # 5035
    # 判断当前时间是否收盘     if close_time > 0:  # 未收盘
    # 当前时间：未收盘=>结束日期为昨天
    # 当前时间：已收盘=>结束日期为今天
    end_date = now_date
    if close_time > 0:  # 未收盘
        sleep_time = close_time  # 给sleep_time赋值
        end_date = yesterday_date  # 如果未收盘，以昨天未结束日期
    for code in stock_list:
        try:  # 如果存在就追加
            data = st.get_csv_data(code=code, data_type='price')
            # 获取最后一天的第二天日期、并转换为时间戳
            last_tomorrow_date = time.mktime(
                time.strptime(data.date[data.date.size - 1],
                              '%Y-%m-%d')) + oneday_time  # numpy.array的size方法类似len， -1是减去表头
            # 时间戳转换为日期
            tomorrow_date = time.strftime('%Y-%m-%d', time.localtime(last_tomorrow_date))  # 表格结束那天的第二天
            data = st.get_single_price(
                stock_code=code,
                freq='daily',
                start_date=tomorrow_date,
                end_date=end_date
            )
            st.export_data(
                data=data,
                filename=code,
                data_type='price',
                mode='a'
            )
        except Exception as err:  # 不存在就新建
            print('当前股票不存在或追加失败，重新存储 csv！', err)
            # start_date='2021-06-29'
            # end_date='2021-06-30'
            data = st.get_single_price(
                stock_code=code,
                freq='daily',
                start_date=start_date,
                end_date=end_date,
            )
            st.export_data(
                data=data,
                filename=code,
                data_type='price',
                mode='w'
            )
        # time.sleep(2)
    return sleep_time


# 定时器
while True:
    sleep_time = timer()
    print('更新完毕！', sleep_time)
    time.sleep(sleep_time)
