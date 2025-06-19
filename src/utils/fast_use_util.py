"""
股票量化交易回测系统 - 工具函数模块
提供各种辅助功能，包括日期转换、股票代码验证等通用工具函数
直接用了
"""

from datetime import datetime, timedelta

from ..core.data import get_single_stock_history_data


def update_date_range(stock_code, date_range_label):

    stock_code = stock_code.strip()
    if validate_stock_code(stock_code):
        stock_df = get_single_stock_history_data(stock_code)
        if not stock_df.empty:
            data_start = stock_df.index.min().date()
            data_end = stock_df.index.max().date()
            date_range_label.config(text=f"数据时间范围：{data_start} 至 {data_end}")
        else:
            date_range_label.config(text="数据时间范围：未获取")
    else:
        date_range_label.config(text="数据时间范围：未获取")

def update_date_range_ctk(stock_code, date_range_label):

    stock_code = stock_code.strip()
    if validate_stock_code(stock_code):
        stock_df = get_single_stock_history_data(stock_code)
        if not stock_df.empty:
            data_start = stock_df.index.min().date()
            data_end = stock_df.index.max().date()
            date_range_label.configure(text=f"数据时间范围：{data_start} 至 {data_end}")
        else:
            date_range_label.configure(text="数据时间范围：未获取")
    else:
        date_range_label.configure(text="数据时间范围：未获取")


def validate_stock_code(code: str) -> bool:
    """
    验证股票代码是否符合中国A股市场规范

    参数:
        code: 股票代码字符串

    返回:
        bool: 股票代码是否有效
    """
    # 有效的A股前缀列表及对应市场
    valid_prefix = {
        '60': '上海主板',
        '688': '科创板',
        '000': '深圳主板',
        '002': '中小板',
        '300': '创业板',
        '001': '深圳主板',
        '003': '深圳主板新股',
        '301': '创业板新股',
        '605': '上海主板新股',
        '603': '上海主板'
    }

    # 基本格式检查
    if not code:
        return False

    code = code.strip()

    if not code.isdigit():
        return False

    if len(code) != 6:
        return False

    # 前缀检查
    for prefix in valid_prefix:
        if code.startswith(prefix):
            return True

    return False


def get_date_input(prompt: str, default_date: datetime = None) -> datetime:
    """
    获取用户输入的日期，并进行格式验证

    参数:
        prompt: 提示信息
        default_date: 默认日期（如果用户未输入）

    返回:
        datetime: 用户输入的日期或默认日期
    """
    while True:
        date_str = input(prompt).strip()
        if not date_str and default_date:
            return default_date
        try:
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
            return parsed_date
        except ValueError:
            print("日期格式错误，请输入 YYYY-MM-DD 格式")


def min2date(start_time: datetime, end_time: datetime) -> tuple:
    """
    将分钟级别的时间转换为适合backtrader使用的日期格式

    参数:
        start_time: 开始时间（实际时间）
        end_time: 结束时间（实际时间）

    返回:
        tuple: 转换后的(开始时间, 结束时间)，基于1970年1月1日
    """
    # 计算开盘时间相对于9:30的分钟数
    start_minutes = (start_time.hour * 60 + start_time.minute) - (9 * 60 + 30)
    end_minutes = (end_time.hour * 60 + end_time.minute) - (9 * 60 + 30)

    # 基准日期（1970年1月1日）
    base_date = datetime(1970, 1, 1)

    # 将分钟数转换为从基准日期开始的天数
    v_start_date = base_date + timedelta(days=start_minutes)
    v_end_date = base_date + timedelta(days=end_minutes)

    return v_start_date, v_end_date


def data_min2date_rename(df):
    """
    暂时作废的函数，传入的类型应当是一个dataframe，里面的index是datetime类型
    """
    minutes = df.index().max() - df.index().min()
    days = int(minutes.total_seconds() / 60)
