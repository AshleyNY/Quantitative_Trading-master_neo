"""
股票量化交易回测系统 - 数据获取模块
负责从外部数据源获取股票历史数据和分时数据，并进行格式转换和预处理
"""

from datetime import datetime, timedelta

import akshare as ak
import pandas as pd


def get_single_stock_history_data(symbol):
    """
    获取单只股票的历史日K线数据

    参数:
        symbol: 股票代码，如'600519'

    返回:
        DataFrame: 包含开盘价、收盘价、最高价、最低价和成交量的数据框
    """
    try:
        # 通过akshare获取后复权数据
        data = ak.stock_zh_a_hist(symbol=symbol, adjust="hfq")[['日期', '开盘', '收盘', '最高', '最低', '成交量']]

        # 重命名列为英文，便于后续处理
        data.columns = ['date', 'open', 'close', 'high', 'low', 'volume']

        # 设置日期索引
        data.index = pd.to_datetime(data['date'])

        # 将价格和成交量列转换为数值类型
        numeric_columns = ['open', 'close', 'high', 'low', 'volume']
        for column in numeric_columns:
            data[column] = pd.to_numeric(data[column], errors='coerce')

        # 填充缺失值
        data[numeric_columns] = data[numeric_columns].ffill().bfill()

        return data
    except Exception as e:
        print(f"数据获取失败: {str(e)}")
        return pd.DataFrame()


def get_single_stock_ticks_data_advanced(stock_code, start, end):
    """
    获取单只股票的分钟级历史数据，保留原始时间格式

    参数:
        stock_code: 股票代码
        start: 开始日期时间
        end: 结束日期时间

    返回:
        DataFrame: 包含原始时间索引的分钟级数据
    """
    try:
        # 获取1分钟K线数据
        data = ak.stock_zh_a_hist_min_em(
            symbol=stock_code,
            start_date=start,
            end_date=end,
            period="1",
            adjust="hfq"
        )[['时间', '开盘', '收盘', '最高', '最低', '成交量']]

        # 重命名列为英文
        data.columns = ['date', 'open', 'close', 'high', 'low', 'volume']

        # 设置日期索引
        data.index = pd.to_datetime(data['date'])

        # 转换为数值类型并处理缺失值
        numeric_columns = ['open', 'close', 'high', 'low', 'volume']
        for column in numeric_columns:
            data[column] = pd.to_numeric(data[column], errors='coerce')
        data[numeric_columns] = data[numeric_columns].ffill().bfill()

        return data
    except Exception as e:
        print(f"数据获取错误: {e}")
        return pd.DataFrame()


def get_single_stock_ticks_data_transfer(stock_code, start, end):
    """
    获取单只股票的分钟级历史数据，并将时间转换为特殊格式以适应backtrader的日期要求

    参数:
        stock_code: 股票代码
        start: 开始日期时间
        end: 结束日期时间

    返回:
        DataFrame: 包含转换后时间索引的分钟级数据
    """
    try:
        # 获取1分钟K线数据
        data = ak.stock_zh_a_hist_min_em(
            symbol=stock_code,
            start_date=start,
            end_date=end,
            period="1",
            adjust="hfq"
        )[['时间', '开盘', '收盘', '最高', '最低', '成交量']]

        # 重命名列为英文
        data.columns = ['date', 'open', 'close', 'high', 'low', 'volume']

        # 设置日期索引
        data.index = pd.to_datetime(data['date'])

        # 时间映射：将分钟数据映射到从1970年开始的日期，以便backtrader处理
        # backtrader不直接支持分钟级回测，使用这种方法将分钟转换为天级别数据
        base_date = datetime(1970, 1, 1)
        new_dates = []

        for dt in data.index:
            # 计算从9:30开始经过的分钟数
            minutes_passed = (dt.hour * 60 + dt.minute) - (9 * 60 + 30)
            # 将分钟数映射为从基准日期开始的天数
            new_date = base_date + timedelta(days=minutes_passed)
            new_dates.append(new_date)

        # 更新索引和日期列
        data.index = pd.DatetimeIndex(new_dates)
        data['date'] = pd.DatetimeIndex(new_dates)

        # 转换为数值类型并处理缺失值
        numeric_columns = ['open', 'close', 'high', 'low', 'volume']
        for column in numeric_columns:
            data[column] = pd.to_numeric(data[column], errors='coerce')
        data[numeric_columns] = data[numeric_columns].ffill().bfill()

        # 修复API返回的开盘价问题（有时为0）
        data['open'] = data.apply(lambda row: row['close'] if row['open'] == 0 else row['open'], axis=1)

        return data
    except Exception as e:
        print(f"数据获取错误: {e}")
        return pd.DataFrame()

def get_single_stock_info(stock_code):
    try:
        info_df = ak.stock_individual_info_em(symbol=stock_code)

        return info_df

    except Exception as e:
        print(f"获取股票信息失败: {e}")

