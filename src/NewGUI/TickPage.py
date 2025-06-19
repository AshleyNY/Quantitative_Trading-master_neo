import customtkinter as ctk
from datetime import datetime
import matplotlib.pyplot as plt
import threading
from src.core.backtest import run_ticks_backtest
import akshare as ak
import pandas as pd


plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

class NewTickPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.last_backtest_engine = None
        

        self.create_tick_content()
    
    def create_tick_content(self):

        title_label = ctk.CTkLabel(
            self, 
            text="⏰ 分时回测策略", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=(20, 30))
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        self.create_parameters_section()
        self.create_control_section()
        self.create_results_section()
    
    def create_parameters_section(self):
        params_frame = ctk.CTkFrame(self.scrollable_frame)
        params_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        params_frame.grid_columnconfigure((0, 1), weight=1)
        basic_frame = ctk.CTkFrame(params_frame)
        basic_frame.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")
        basic_frame.grid_columnconfigure(1, weight=1)

        basic_title = ctk.CTkLabel(
            basic_frame, 
            text="基本参数", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        basic_title.grid(row=0, column=0, columnspan=2, pady=(15, 20))
        

        ctk.CTkLabel(basic_frame, text="股票代码:", font=ctk.CTkFont(size=14)).grid(
            row=1, column=0, padx=(20, 10), pady=10, sticky="w"
        )
        self.stock_code_entry = ctk.CTkEntry(basic_frame, placeholder_text="请输入6位股票代码")
        self.stock_code_entry.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="ew")
        self.stock_code_entry.insert(0, "000001")
        self.stock_code_entry.bind("<KeyRelease>", self.update_date_range)

        self.market_label = ctk.CTkLabel(
            basic_frame, 
            text="市场：深圳主板", 
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.market_label.grid(row=2, column=1, padx=(0, 20), sticky="w")

        ctk.CTkLabel(basic_frame, text="交易日期:", font=ctk.CTkFont(size=14)).grid(
            row=3, column=0, padx=(20, 10), pady=10, sticky="w"
        )
        self.trade_date_entry = ctk.CTkEntry(basic_frame, placeholder_text="YYYY-MM-DD")
        self.trade_date_entry.grid(row=3, column=1, padx=(0, 20), pady=10, sticky="ew")

        try:
            trade_cal = ak.tool_trade_date_hist_sina()
            today = pd.Timestamp.today().normalize()
            if 'is_open' in trade_cal.columns:
                trade_days = pd.to_datetime(trade_cal[trade_cal['is_open']==1]['trade_date'])
            elif 'flag' in trade_cal.columns:
                trade_days = pd.to_datetime(trade_cal[trade_cal['flag']=='交易']['trade_date'])
            else:
                trade_days = pd.to_datetime(trade_cal['trade_date'])
            trade_days = trade_days[trade_days <= today]
            last_trade_day = trade_days.max().strftime("%Y-%m-%d") if not trade_days.empty else today.strftime("%Y-%m-%d")
        except:
            last_trade_day = datetime.now().strftime("%Y-%m-%d")
        
        self.trade_date_entry.insert(0, last_trade_day)
        

        date_note = ctk.CTkLabel(
            basic_frame, 
            text="(仅支持最近7个交易日)", 
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        date_note.grid(row=4, column=1, padx=(0, 20), sticky="w")
        

        ctk.CTkLabel(basic_frame, text="初始资金:", font=ctk.CTkFont(size=14)).grid(
            row=5, column=0, padx=(20, 10), pady=10, sticky="w"
        )
        self.start_cash_entry = ctk.CTkEntry(basic_frame, placeholder_text="初始资金金额")
        self.start_cash_entry.grid(row=5, column=1, padx=(0, 20), pady=(10, 20), sticky="ew")
        self.start_cash_entry.insert(0, "100000000")

        strategy_frame = ctk.CTkFrame(params_frame)
        strategy_frame.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")
        strategy_frame.grid_columnconfigure(1, weight=1)
        
        strategy_title = ctk.CTkLabel(
            strategy_frame, 
            text="策略参数", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        strategy_title.grid(row=0, column=0, columnspan=2, pady=(15, 20))

        ctk.CTkLabel(strategy_frame, text="价格均线周期(分钟):", font=ctk.CTkFont(size=14)).grid(
            row=1, column=0, padx=(20, 10), pady=10, sticky="w"
        )
        self.price_period_entry = ctk.CTkEntry(strategy_frame, placeholder_text="价格均线周期")
        self.price_period_entry.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="ew")
        self.price_period_entry.insert(0, "10")
        

        ctk.CTkLabel(strategy_frame, text="成交量均线周期(分钟):", font=ctk.CTkFont(size=14)).grid(
            row=2, column=0, padx=(20, 10), pady=10, sticky="w"
        )
        self.volume_period_entry = ctk.CTkEntry(strategy_frame, placeholder_text="成交量均线周期")
        self.volume_period_entry.grid(row=2, column=1, padx=(0, 20), pady=10, sticky="ew")
        self.volume_period_entry.insert(0, "10")
        

        ctk.CTkLabel(strategy_frame, text="止盈比例:", font=ctk.CTkFont(size=14)).grid(
            row=3, column=0, padx=(20, 10), pady=10, sticky="w"
        )
        self.take_profit_entry = ctk.CTkEntry(strategy_frame, placeholder_text="止盈比例")
        self.take_profit_entry.grid(row=3, column=1, padx=(0, 20), pady=10, sticky="ew")
        self.take_profit_entry.insert(0, "1.20")
        

        ctk.CTkLabel(strategy_frame, text="止损比例:", font=ctk.CTkFont(size=14)).grid(
            row=4, column=0, padx=(20, 10), pady=10, sticky="w"
        )
        self.stop_loss_entry = ctk.CTkEntry(strategy_frame, placeholder_text="止损比例")
        self.stop_loss_entry.grid(row=4, column=1, padx=(0, 20), pady=10, sticky="ew")
        self.stop_loss_entry.insert(0, "0.90")

        switches_frame = ctk.CTkFrame(strategy_frame)
        switches_frame.grid(row=5, column=0, columnspan=2, padx=20, pady=(20, 20), sticky="ew")
        
        self.use_tp_var = ctk.BooleanVar(value=True)
        self.use_tp_switch = ctk.CTkCheckBox(
            switches_frame, 
            text="启用止盈", 
            variable=self.use_tp_var,
            font=ctk.CTkFont(size=14)
        )
        self.use_tp_switch.pack(pady=5)
        
        self.use_sl_var = ctk.BooleanVar(value=True)
        self.use_sl_switch = ctk.CTkCheckBox(
            switches_frame, 
            text="启用止损", 
            variable=self.use_sl_var,
            font=ctk.CTkFont(size=14)
        )
        self.use_sl_switch.pack(pady=5)
        
        self.use_price_ma_var = ctk.BooleanVar(value=True)
        self.use_price_ma_switch = ctk.CTkCheckBox(
            switches_frame, 
            text="启用价格均线策略", 
            variable=self.use_price_ma_var,
            font=ctk.CTkFont(size=14)
        )
        self.use_price_ma_switch.pack(pady=5)
        
        self.use_volume_ma_var = ctk.BooleanVar(value=True)
        self.use_volume_ma_switch = ctk.CTkCheckBox(
            switches_frame, 
            text="启用成交量均线策略", 
            variable=self.use_volume_ma_var,
            font=ctk.CTkFont(size=14)
        )
        self.use_volume_ma_switch.pack(pady=5)
    
    def create_control_section(self):

        control_frame = ctk.CTkFrame(self.scrollable_frame)
        control_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.start_button = ctk.CTkButton(
            control_frame,
            text="🚀 开始分时回测",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            command=self.run_backtest
        )
        self.start_button.pack(pady=20)
        

        self.progress_bar = ctk.CTkProgressBar(control_frame)
        self.progress_bar.pack(pady=(0, 20), padx=40, fill="x")
        self.progress_bar.set(0)
    
    def create_results_section(self):

        results_frame = ctk.CTkFrame(self.scrollable_frame)
        results_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(1, weight=1)
        
        results_title = ctk.CTkLabel(
            results_frame, 
            text="📊 分时回测结果", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        results_title.grid(row=0, column=0, pady=(15, 10))
        

        self.result_text = ctk.CTkTextbox(
            results_frame,
            height=300,
            font=ctk.CTkFont(size=12)
        )
        self.result_text.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.result_text.insert("0.0", "等待分时回测开始...")
    
    def update_date_range(self, event=None):

        try:
            stock_code = self.stock_code_entry.get().strip()
            if len(stock_code) == 6 and stock_code.isdigit():
                if stock_code.startswith('0') or stock_code.startswith('3'):
                    self.market_label.configure(text="市场：深圳交易所")
                elif stock_code.startswith('6'):
                    self.market_label.configure(text="市场：上海交易所")
                else:
                    self.market_label.configure(text="市场：未知市场")
            else:
                self.market_label.configure(text="市场：请输入正确代码")
        except Exception as e:
            print(f"更新日期范围时出错: {e}")
    
    def run_backtest(self):

        self.start_button.configure(state="disabled", text="分时回测中...")
        self.progress_bar.set(0.1)
        
        thread = threading.Thread(target=self._run_backtest_thread)
        thread.daemon = True
        thread.start()
    
    def _run_backtest_thread(self):

        try:
            stock_code = self.stock_code_entry.get().strip()
            trade_date_str = self.trade_date_entry.get().strip()
            start_cash = float(self.start_cash_entry.get().strip())
            price_period = int(self.price_period_entry.get().strip())
            volume_period = int(self.volume_period_entry.get().strip())
            take_profit = float(self.take_profit_entry.get().strip())
            stop_loss = float(self.stop_loss_entry.get().strip())
            

            use_tp = self.use_tp_var.get()
            use_sl = self.use_sl_var.get()
            use_price_ma = self.use_price_ma_var.get()
            use_volume_ma = self.use_volume_ma_var.get()
            
            self.progress_bar.set(0.3)
            try:
                trade_date = datetime.strptime(trade_date_str, "%Y-%m-%d")
            except ValueError:
                print("日期格式错误", "请使用YYYY-MM-DD格式输入日期")
                return

            result, backtest_engine = run_ticks_backtest(
                stock_code=stock_code,
                date=trade_date,
                start_cash=start_cash,
                price_period=price_period,
                volume_period=volume_period,
                profit_rate=take_profit,
                loss_rate=stop_loss,
                stop_by_profit=use_tp,
                stop_by_loss=use_sl,
                use_price_ma=use_price_ma,
                use_volume_ma=use_volume_ma,
                profit_size=1000,
                loss_size=1000,
                buy_size=1000,
                sell_size=1000
            )
            if result and backtest_engine:
                self.progress_bar.set(0.8)
                self.last_backtest_engine = backtest_engine

                self.result_text.delete("0.0", "end")
                self.result_text.insert("0.0", result)

                self.progress_bar.set(1.0)

                strategy_instance = backtest_engine.runstrats[0][0]
                backtest_engine.plot(
                    style='candlestick',
                    iplot=False,
                    barup='red',
                    bardown='green',
                    title=f'{stock_code} 回测结果\n{trade_date.strftime("%Y-%m-%d")}',
                    grid=True,
                    figsize=(14, 7),
                )



            
        except Exception as e:
            error_msg = f"分时回测过程中发生错误：\n{str(e)}"
            self.result_text.delete("0.0", "end")
            self.result_text.insert("0.0", error_msg)
        
        finally:

            self.start_button.configure(state="normal", text="🚀 开始分时回测")

            self.after_idle(lambda: self.progress_bar.set(0))