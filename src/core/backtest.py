"""
股票量化交易回测系统 - 回测核心模块
负责执行日K线和分时数据的回测逻辑，生成回测报告和结果
"""

from datetime import datetime, time
from tkinter import messagebox

import backtrader as bt

from src.core.data import get_single_stock_history_data, \
    get_single_stock_ticks_data_transfer
from src.core.strategy import DailyMA, SuperShortLineTrade
from src.utils.fast_use_util import min2date


def run_daily_backtest(stock_code, use_take_profit, take_profit, take_profit_size,
                       use_stop_loss, stop_loss, stop_loss_size,
                       use_sma_crossover, fast_maperiod, slow_maperiod,
                       start_cash, sma_buy_size=None, sma_sell_size=None, start_date=None, end_date=None):
    """
    执行日K线回测

    参数:
        stock_code: 股票代码
        use_take_profit: 是否启用止盈
        take_profit: 止盈比例
        take_profit_size: 止盈交易笔数
        use_stop_loss: 是否启用止损
        stop_loss: 止损比例
        stop_loss_size: 止损交易笔数
        use_sma_crossover: 是否使用均线交叉策略
        fast_maperiod: 快速均线周期
        slow_maperiod: 慢速均线周期
        start_cash: 初始资金
        sma_buy_size: 均线买入笔数
        sma_sell_size: 均线卖出笔数
        start_date: 回测起始日期
        end_date: 回测结束日期

    返回:
        tuple: (回测报告字符串, 回测引擎实例)
    """
    # 获取股票历史数据
    stock_data = get_single_stock_history_data(stock_code)
    if stock_data.empty:
        print("未找到对应股票数据，请检查代码格式（A股6位数字代码）")
        return None, None

    # 设置默认日期范围
    if not start_date:
        start_date = datetime.combine(stock_data.index.min().date(), datetime.min.time())
    if not end_date:
        end_date = datetime.combine(stock_data.index.max().date(), datetime.min.time())

    # 验证并调整日期范围
    data_start = stock_data.index.min().date()
    data_end = stock_data.index.max().date()

    # 调整开始日期
    if start_date.date() < data_start:
        print(f"警告：开始日期早于数据最早日期 ({data_start})，已自动修正")
        start_date = datetime.combine(data_start, datetime.min.time())
    elif start_date.date() > data_end:
        print(f"警告：开始日期晚于数据最新日期 ({data_end})，已自动修正")
        start_date = datetime.combine(data_end, datetime.min.time())

    # 调整结束日期
    if end_date.date() > data_end:
        print(f"警告：结束日期晚于数据最新日期 ({data_end})，已自动修正")
        end_date = datetime.combine(data_end, datetime.min.time())
    elif end_date.date() < data_start:
        print(f"警告：结束日期早于数据最早日期 ({data_start})，已自动修正")
        end_date = datetime.combine(data_start, datetime.min.time())

    # 确保开始日期早于结束日期
    if start_date > end_date:
        print(f"错误：开始日期 {start_date.date()} 晚于结束日期 {end_date.date()}，已自动交换")
        start_date, end_date = end_date, start_date

    # 验证均线参数
    if use_sma_crossover:
        try:
            fast_ma = int(fast_maperiod)
            slow_ma = int(slow_maperiod)
            if not (5 <= fast_ma < slow_ma <= 30):
                messagebox.showerror("错误", "快线周期应小于慢线周期，且范围在5-30之间")
                return None, None
        except ValueError:
            messagebox.showerror("错误", "均线周期必须为整数")
            return None, None

    # 创建回测引擎
    back_test_engine = bt.Cerebro()
    data = bt.feeds.PandasData(dataname=stock_data, fromdate=start_date, todate=end_date)
    back_test_engine.adddata(data)

    # 添加交易策略
    back_test_engine.addstrategy(
        DailyMA,
        start_date=start_date,
        end_date=end_date,
        fast_maperiod=fast_maperiod,
        slow_maperiod=slow_maperiod,
        stop_loss=stop_loss,
        take_profit=take_profit,
        use_take_profit=use_take_profit,
        use_stop_loss=use_stop_loss,
        use_sma_crossover=use_sma_crossover,
        take_profit_size=take_profit_size,
        stop_loss_size=stop_loss_size,
        sma_buy_size=sma_buy_size if sma_buy_size is not None else take_profit_size,
        sma_sell_size=sma_sell_size if sma_sell_size is not None else stop_loss_size
    )

    # 设置初始资金和分析器
    back_test_engine.broker.setcash(start_cash)
    back_test_engine.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    back_test_engine.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade')

    # 执行回测
    results = back_test_engine.run()
    strat = results[0]

    # 分析回测结果
    drawdown_analysis = strat.analyzers.drawdown.get_analysis() if hasattr(strat.analyzers, 'drawdown') else {}
    drawdown_value = drawdown_analysis.get('max', {}).get('drawdown', 0.0) if isinstance(drawdown_analysis, dict) else 0.0
    port_value = back_test_engine.broker.getvalue()
    pnl = port_value - start_cash

    # 计算交易次数
    trade_count = 0
    if hasattr(strat.analyzers, 'trade'):
        trade_analysis = strat.analyzers.trade.get_analysis()
        try:
            trade_count = trade_analysis['total']['closed']
        except KeyError:
            trade_count = 0

    # 生成回测报告
    report = f"\n{'=' * 30} 回测报告 {'=' * 30}\n"
    report += f"股票代码: {stock_code}\n"
    report += f"回测时间: {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}\n"
    report += f"初始资金: {start_cash:,.2f} 元\n"
    report += f"总资金: {port_value:,.2f} 元\n"
    report += f"净收益: {pnl:,.2f} 元\n"
    report += f"收益率: {pnl / start_cash * 100:.2f}%\n"

    # 添加策略参数信息
    report += f"止盈功能: {'开启' if use_take_profit else '关闭'}\n"
    if use_take_profit:
        report += f"止盈比例: {take_profit * 100:.2f}% | 止盈交易笔数: {take_profit_size} 股\n"
    else:
        report += "止盈功能已关闭\n"

    report += f"止损功能: {'开启' if use_stop_loss else '关闭'}\n"
    if use_stop_loss:
        report += f"止损比例: {stop_loss * 100:.2f}% | 止损交易笔数: {stop_loss_size} 股\n"
    else:
        report += "止损功能已关闭\n"

    report += f"均线交易: {'开启' if use_sma_crossover else '关闭'}\n"
    if use_sma_crossover:
        report += f"均线周期: 快线={fast_maperiod}日 | 慢线={slow_maperiod}日\n"
        report += f"均线买入笔数: {sma_buy_size if sma_buy_size is not None else take_profit_size} 股 | "
        report += f"均线卖出笔数: {sma_sell_size if sma_sell_size is not None else stop_loss_size} 股\n"
    else:
        report += "均线功能已关闭\n"

    # 添加绩效统计信息
    report += f"最大回撤: {float(drawdown_value):.2f}%\n" if drawdown_value and float(drawdown_value) > 0 else "最大回撤: N/A (未触发持仓变动)\n"
    report += f"交易次数: {trade_count} 次\n"
    report += '=' * 70

    return report, back_test_engine


def run_ticks_backtest(stock_code,
                       price_period,
                       volume_period,
                       stop_by_profit,
                       profit_rate,
                       profit_size,
                       stop_by_loss,
                       loss_rate,
                       loss_size,
                       buy_size,
                       sell_size,
                       start_cash, date,
                       use_price_ma=True,
                       use_volume_ma=True):
    """
    执行分时数据回测

    参数:
        stock_code: 股票代码
        price_period: 价格周期
        volume_period: 成交量周期
        stop_by_profit: 是否启用止盈
        profit_rate: 止盈比例
        profit_size: 止盈交易笔数
        stop_by_loss: 是否启用止损
        loss_rate: 止损比例
        loss_size: 止损交易笔数
        buy_size: 买入笔数
        sell_size: 卖出笔数
        start_cash: 初始资���
        date: 回测日期
        use_price_ma: 是否使用价格均线
        use_volume_ma: 是否使用交易量均线

    返回:
        tuple: (回测报告字符串, 回测引擎实例)
    """
    # 设置交易时间范围
    opentime = time(hour=9, minute=30, second=0)
    closetime = time(hour=15, minute=0)
    real_start_date = datetime.combine(date, opentime)
    real_end_date = datetime.combine(date, closetime)

    # 获取股票分时数据
    stock_data = get_single_stock_ticks_data_transfer(stock_code, real_start_date, real_end_date)
    if stock_data.empty:
        print("未找到对应股票数据，请检查代码格式（A股6位数字代码）")
        return None, None

    # 映射虚拟日期范围
    v_start_date, v_end_date = min2date(real_start_date, real_end_date)

    # 创建回测引擎
    back_test_ticks_engine = bt.Cerebro()
    data = bt.feeds.PandasData(dataname=stock_data, fromdate=v_start_date, todate=v_end_date)
    back_test_ticks_engine.adddata(data)

    # 添加交易策略
    back_test_ticks_engine.addstrategy(
        SuperShortLineTrade,
        start_date=v_start_date,
        end_date=v_end_date,
        price_period=price_period,
        volume_period=volume_period,
        profit_rate=profit_rate,
        profit_size=profit_size,
        stop_by_profit=stop_by_profit,
        loss_rate=loss_rate,
        loss_size=loss_size,
        stop_by_loss=stop_by_loss,
        buy_size=buy_size,
        sell_size=sell_size,
        use_price_ma=use_price_ma,
        use_volume_ma=use_volume_ma
    )

    # 设置初始资金和分析器
    back_test_ticks_engine.broker.setcommission(commission=0.005)
    back_test_ticks_engine.broker.setcash(start_cash)
    back_test_ticks_engine.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    back_test_ticks_engine.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade')

    # 执行回测
    results = back_test_ticks_engine.run()
    strat = results[0]

    # 分析回测结果
    drawdown_analysis = strat.analyzers.drawdown.get_analysis() if hasattr(strat.analyzers, 'drawdown') else {}
    drawdown_value = drawdown_analysis.get('max', {}).get('drawdown', 0.0) if isinstance(drawdown_analysis, dict) else 0.0
    port_value = back_test_ticks_engine.broker.getvalue()
    pnl = port_value - start_cash

    # 计算交易次数
    trade_count = 0
    if hasattr(strat.analyzers, 'trade'):
        trade_analysis = strat.analyzers.trade.get_analysis()
        try:
            trade_count = trade_analysis['total']['closed']
        except KeyError:
            trade_count = 0

    # 生成回测报告
    report = f"\n{'=' * 30} 回测报告 {'=' * 30}\n"
    report += f"股票代码: {stock_code}\n"
    report += f"回测时间: {real_start_date.strftime('%Y-%m-%d %H:%M:%S')} 至 {real_end_date.strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"初始资金: {start_cash:,.2f} 元\n"
    report += f"总资金: {port_value:,.2f} 元\n"
    report += f"净收益: {pnl:,.2f} 元\n"
    report += f"收益率: {pnl / start_cash * 100:.2f}%\n"

    # 添加策略参数信息
    report += f"止盈功能: {'开启' if stop_by_profit else '关闭'}\n"
    if stop_by_profit:
        report += f"止盈比例: {profit_rate * 100:.2f}% | 止盈交易笔数: {profit_size} 股\n"
    else:
        report += "止盈功能已关闭\n"

    report += f"止损功能: {'开启' if stop_by_loss else '关闭'}\n"
    if stop_by_loss:
        report += f"止损比例: {loss_rate * 100:.2f}% | 止损交易笔数: {loss_size} 股\n"
    else:
        report += "止损功能已关闭\n"

    # 添加绩效统计信息
    report += f"最大回撤: {float(drawdown_value):.2f}%\n" if drawdown_value and float(drawdown_value) > 0 else "最大回撤: N/A (未触发持仓变动)\n"
    report += f"交易次数: {trade_count} 次\n"
    report += '=' * 70

    return report, back_test_ticks_engine
