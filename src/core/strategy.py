"""
股票量化交易回测系统 - 交易策略模块
该模块定义了系统中使用的各种交易策略类
"""

import backtrader as bt


class DailyMA(bt.Strategy):
    """
    日K线均线交易策略

    基于快速均线和慢速均线的金叉死叉进行交易，同时支持止盈止损功能

    参数:
        fast_maperiod (int): 快速均线周期，默认为5日
        slow_maperiod (int): 慢速均线周期，默认为30日
        start_date: 回测开始日期
        end_date: 回测结束日期
        stop_loss (float): 止损比例，默认为0.95（亏损5%止损）
        take_profit (float): 止盈比例，默认为1.1（盈利10%止盈）
        use_take_profit (bool): 是否启用止盈
        use_stop_loss (bool): 是否启用止损
        use_sma_crossover (bool): 是否启用均线交叉策略
        take_profit_size (int): 止盈交易笔数
        stop_loss_size (int): 止损交易笔数
        sma_buy_size (int): 均线买入交易笔数
        sma_sell_size (int): 均线卖出交易笔数
    """

    params = (
        ("fast_maperiod", 5),
        ("slow_maperiod", 30),
        ("start_date", None),
        ("end_date", None),
        ("stop_loss", 0.95),
        ("take_profit", 1.1),
        ("use_take_profit", False),
        ("use_stop_loss", False),
        ("use_sma_crossover", False),
        ("take_profit_size", 1000),
        ("stop_loss_size", 1000),
        ("sma_buy_size", 1000),
        ("sma_sell_size", 1000)
    )

    def __init__(self):
        """初始化策略，设置数据和指标"""
        # 获取收盘价数据
        self.data_close = self.datas[0].close
        # 初始化订单和买入价格
        self.order = None
        self.buy_price = None

        # 如果启用均线交叉策略，则创建相应的均线指标
        if self.p.use_sma_crossover:
            # 计算快速均线
            self.fast_sma = bt.indicators.SimpleMovingAverage(
                self.datas[0].close,
                period=self.p.fast_maperiod
            )
            # 计算慢速均线
            self.slow_sma = bt.indicators.SimpleMovingAverage(
                self.datas[0].close,
                period=self.p.slow_maperiod
            )
            # 创建均线交叉指标
            self.crossover = bt.indicators.CrossOver(self.fast_sma, self.slow_sma)

    def log(self, txt):
        """
        记录策略日志

        参数:
            txt (str): 日志内容
        """
        dt = self.datas[0].datetime.date(0)
        print(f"{dt.isoformat()} - {txt}")

    def notify_order(self, order):
        """
        订单状态变化通知

        参数:
            order: 交易订单对象
        """
        # 判断订单是否完成
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f"已买入，价格: {order.executed.price:.2f}, 数量: {order.executed.size}")
                self.buy_price = order.executed.price
            else:
                self.log(f"已卖出，价格: {order.executed.price:.2f}, 数量: {order.executed.size}")
            # 重置订单状态
            self.order = None

    def next(self):
        """
        策略核心逻辑，每个交易日调用一次

        根据均线交叉和止盈止损条件进行交易决策
        """
        # 如果有未完成的订单，跳过循环0
        if self.order:
            return

        # 获取当前日期，并检查是否在回测范围内
        current_date = self.datas[0].datetime.date(0)
        if (self.p.start_date and current_date < self.p.start_date.date()) or \
                (self.p.end_date and current_date > self.p.end_date.date()):
            return

        # 当前没有持仓时的买入逻辑
        if not self.position:
            # 均线金叉买入信号
            if self.p.use_sma_crossover and self.crossover > 0:
                self.order = self.buy(size=self.p.sma_buy_size)
        # 当前有持仓时的卖出逻辑
        else:
            # 均线死叉卖出信号
            if self.p.use_sma_crossover and self.crossover < 0:
                self.order = self.sell(size=self.p.sma_sell_size)
            # 止盈逻辑
            if self.p.use_take_profit and self.buy_price and self.data_close[0] >= self.buy_price * self.p.take_profit:
                self.order = self.sell(size=self.p.take_profit_size)
            # 止损逻辑
            elif self.p.use_stop_loss and self.buy_price and self.data_close[0] < self.buy_price * self.p.stop_loss:
                self.order = self.sell(size=self.p.stop_loss_size)


class SuperShortLineTrade(bt.Strategy):
    """
    分时交易策略 - 超短线交易

    基于价格和成交量的均线交叉进行交易，同时支持止盈止损功能

    参数:
        start_date: 回测开始日期
        end_date: 回测结束日期
        price_period (int): 价格均线周期，默认为5分钟
        volume_period (int): 成交量均线周期，默认为5分钟
        buy_size (int): 主策略买入交易笔数
        sell_size (int): 主策略卖出交易笔数
        stop_by_profit (bool): 是否启用止盈
        profit_size (int): 止盈交易笔数
        profit_rate (float): 止盈比例，默认为1.1（盈利10%止盈）
        stop_by_loss (bool): 是否启用止损
        loss_size (int): 止损交易笔数
        loss_rate (float): 止损比例，默认为0.9（亏损10%止损）
        use_price_ma (bool): 是否启用价格均线
        use_volume_ma (bool): 是否启用成交量均线
    """

    params = (
        ("start_date", None),
        ("end_date", None),
        ('price_period', 5),     # 价格均线周期（分钟）
        ('volume_period', 5),    # 成交量均线周期（分钟）
        ("buy_size", 1000),      # 买入交易笔数
        ("sell_size", 1000),     # 卖出交易笔数
        ("stop_by_profit", False), # 是否启用止盈
        ("profit_size", 1000),   # 止盈交易笔数
        ("profit_rate", 1.1),    # 止盈比例
        ("stop_by_loss", False), # 是否启用止损
        ("loss_size", 1000),     # 止损交易笔数
        ("loss_rate", 0.9),      # 止损比例
        ("use_price_ma", True),  # 是否启用价格均线
        ("use_volume_ma", True), # 是否启用成交量均线
    )

    def __init__(self):
        """初始化策略，设置数据和指标"""
        # 获取价格和成交量数据
        self.data_price = self.datas[0].close  # 收盘价
        self.data_volume = self.datas[0].volume  # 成交量

        # 初始化变量
        self.order = None        # 当前订单
        self.buy_price = None    # 买入价格
        self.trades = []         # 交易记录

        # 创建价格均线和交叉指标
        self.price_sma = bt.indicators.SimpleMovingAverage(
            self.data_price,
            period=self.p.price_period,
            plotname="price_sma"
        )
        self.price_crossover = bt.indicators.CrossOver(self.data_price, self.price_sma)

        # 创建成交量均线和交叉指标
        self.volume_sma = bt.indicators.SimpleMovingAverage(
            self.data_volume,
            period=self.p.volume_period,
        )
        self.volume_crossover = bt.indicators.CrossOver(self.data_volume, self.volume_sma)

    def log(self, txt):
        """
        记录策略日志

        参数:
            txt (str): 日志内容
        """
        dt = self.datas[0].datetime.date(0)
        print(f"{dt.isoformat()} - {txt}")

    def notify_order(self, order):
        """
        订单状态变化通知

        参数:
            order: 交易订单对象
        """
        # 如果订单正在处理中，则跳过
        if order.status in [order.Submitted, order.Accepted]:
            return

        # 判断订单是否完成
        if order.status in [order.Completed]:
            dt = self.datas[0].datetime.datetime(0)

            # 买入订单完成
            if order.isbuy():
                self.buy_price = order.executed.price
                self.log(f"买入: 价格={order.executed.price:.2f}, 数量={order.executed.size:.2f}")
                # 记录交易
                self.trades.append({
                    'datetime': dt.strftime('%Y-%m-%d %H:%M:%S'),
                    'type': '买入',
                    'price': order.executed.price,
                    'size': order.executed.size
                })
            # 卖出订单完成
            else:
                self.log(f"卖出: 价格={order.executed.price:.2f}, 数量={order.executed.size:.2f}")
                # 记录交易
                self.trades.append({
                    'datetime': dt.strftime('%Y-%m-%d %H:%M:%S'),
                    'type': '卖出',
                    'price': order.executed.price,
                    'size': order.executed.size
                })

        # 重置订单状态
        self.order = None

    def next(self):
        """
        策略核心逻辑，每个交易周期调用一次

        根据价格均线交叉和止盈止损条件进行交易决策
        """
        # 如果有未完成的订单，跳过本次循环
        if self.order:
            return

        # 获取当前日期，并检查是否在回测范围内
        current_date = self.datas[0].datetime.date(0)
        if (self.p.start_date and current_date < self.p.start_date.date()) or \
                (self.p.end_date and current_date > self.p.end_date.date()):
            return

        # 获取当前价格
        current_price = self.data_price[0]

        # 当前没有持仓时的买入逻辑
        if not self.position:
            # 价格均线买入逻辑
            if self.p.use_price_ma and self.price_crossover < 0:
                self.order = self.buy(size=self.p.buy_size)
            # 交易量均线买入逻辑
            elif self.p.use_volume_ma and self.volume_crossover < 0:
                self.order = self.buy(size=self.p.buy_size)
        # 当前有持仓时的卖出逻辑
        else:
            # 止损逻辑
            if self.p.stop_by_loss and self.buy_price and current_price <= self.buy_price * self.p.loss_rate:
                self.order = self.sell(size=self.p.loss_size)
                self.log(f"卖出：止损 卖出股数：{self.p.loss_size} 当前价格：{current_price}")
            # 止盈逻辑
            elif self.p.stop_by_profit and self.buy_price and current_price >= self.buy_price * self.p.profit_rate:
                self.order = self.sell(size=self.p.profit_size)
                self.log(f"卖出：止盈 卖出股数：{self.p.profit_size} 当前价格：{current_price}")
            # 价格均线卖出逻辑
            elif self.p.use_price_ma and self.price_crossover > 0:
                self.order = self.sell(size=self.p.sell_size)
            # 交易量均线卖出逻辑
            elif self.p.use_volume_ma and self.volume_crossover > 0:
                self.order = self.sell(size=self.p.sell_size)

        # 注：以下是原量价分析策略的代码，已注释掉
        """
        # 量价分析策略:
        # 放量上升：买入
        # 缩量上升：卖出
        # 缩量下降：买入
        # 放量下降：卖出
        # 无趋势：无操作
        
        # 当前无持仓时
        if not self.position:
            # 放量上涨
            if self.volume_crossover > 0 and self.price_crossover > 0:
                self.order = self.buy(size=self.p.buy_size)
                self.log(f"买入：放量上涨 买入股数：{self.p.buy_size} 当前价格：{current_price}")
            # 缩量下跌
            if self.volume_crossover < 0 and self.price_crossover < 0:
                self.order = self.buy(size=self.p.buy_size)
                self.log(f"买入：缩量下跌 买入股数：{self.p.buy_size} 当前价格：{current_price}")
        # 当前有持仓时
        else:
            # 缩量上涨
            if self.volume_crossover < 0 < self.price_crossover:
                self.order = self.sell(size=self.p.sell_size)
                self.log(f"卖出：缩量上涨 卖出股数：{self.p.sell_size} 当前价格：{current_price}")
            # 放量下跌
            if self.volume_crossover > 0 > self.price_crossover:
                self.order = self.sell(size=self.p.sell_size)
                self.log(f"卖出：放量下跌 卖出股数：{self.p.sell_size} 当前价格：{current_price}")
        """
