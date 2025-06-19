
import customtkinter as ctk

from datetime import datetime, timedelta

import matplotlib.pyplot as plt

import threading

from ..core.backtest import run_daily_backtest
from ..utils.fast_use_util import update_date_range_ctk

plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

class NewDailyPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.last_backtest_engine = None
        self.create_daily_content()
    
    def create_daily_content(self):
        title_label = ctk.CTkLabel(
            self, 
            text="日K回测策略",
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
        self.stock_code_entry.insert(0, "")
        self.stock_code_entry.bind("<KeyRelease>", self.update_date_range)
        

        self.market_label = ctk.CTkLabel(
            basic_frame, 
            text="市场：输入代码获取",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        self.market_label.grid(row=2, column=1, padx=(0, 20), sticky="w")

        self.date_label = ctk.CTkLabel(
            basic_frame,
            text="有效日期:输入代码获取",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        self.date_label.grid(row=3, column=1, padx=(0, 20), sticky="w")
        

        ctk.CTkLabel(basic_frame, text="开始日期:", font=ctk.CTkFont(size=14)).grid(
            row=4, column=0, padx=(20, 10), pady=10, sticky="w"
        )
        self.start_date_entry = ctk.CTkEntry(basic_frame, placeholder_text="YYYY-MM-DD")
        self.start_date_entry.grid(row=4, column=1, padx=(0, 20), pady=10, sticky="ew")
        default_start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        self.start_date_entry.insert(0, default_start_date)
        

        ctk.CTkLabel(basic_frame, text="结束日期:", font=ctk.CTkFont(size=14)).grid(
            row=5, column=0, padx=(20, 10), pady=10, sticky="w"
        )
        self.end_date_entry = ctk.CTkEntry(basic_frame, placeholder_text="YYYY-MM-DD")
        self.end_date_entry.grid(row=5, column=1, padx=(0, 20), pady=10, sticky="ew")
        default_end_date = datetime.now().strftime("%Y-%m-%d")
        self.end_date_entry.insert(0, default_end_date)

        ctk.CTkLabel(basic_frame, text="初始资金:", font=ctk.CTkFont(size=14)).grid(
            row=6, column=0, padx=(20, 10), pady=10, sticky="w"
        )
        self.start_cash_entry = ctk.CTkEntry(basic_frame, placeholder_text="初始资金金额")
        self.start_cash_entry.grid(row=6, column=1, padx=(0, 20), pady=(10, 20), sticky="ew")
        self.start_cash_entry.insert(0, "100000000")
        

        strategy_frame = ctk.CTkFrame(params_frame)
        strategy_frame.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")
        strategy_frame.grid_columnconfigure(3, weight=1)
        
        strategy_title = ctk.CTkLabel(
            strategy_frame, 
            text="策略参数", 
            font=ctk.CTkFont(size=18, weight="bold")

        )
        strategy_title.grid(row=0, column=1, pady=(15, 20), sticky="ew")
        

        ctk.CTkLabel(strategy_frame, text="快线周期:", font=ctk.CTkFont(size=14)).grid(
            row=1, column=0, padx=(20, 10), pady=10, sticky="w"
        )
        self.fast_ma_entry = ctk.CTkEntry(strategy_frame, placeholder_text="快线周期")
        self.fast_ma_entry.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="ew")
        self.fast_ma_entry.insert(0, "5")
        

        ctk.CTkLabel(strategy_frame, text="慢线周期:", font=ctk.CTkFont(size=14)).grid(
            row=1, column=2, padx=(20, 10), pady=10, sticky="w"
        )
        self.slow_ma_entry = ctk.CTkEntry(strategy_frame, placeholder_text="慢线周期")
        self.slow_ma_entry.grid(row=1, column=3, padx=(0, 20), pady=10, sticky="ew")
        self.slow_ma_entry.insert(0, "30")
        

        ctk.CTkLabel(strategy_frame, text="止盈比例:", font=ctk.CTkFont(size=14)).grid(
            row=2, column=0, padx=(20, 10), pady=10, sticky="w"
        )
        self.take_profit_entry = ctk.CTkEntry(strategy_frame, placeholder_text="止盈比例")
        self.take_profit_entry.grid(row=2, column=1, padx=(0, 20), pady=10, sticky="ew")
        self.take_profit_entry.insert(0, "1.2")
        

        ctk.CTkLabel(strategy_frame, text="止损比例:", font=ctk.CTkFont(size=14)).grid(
            row=2, column=2, padx=(20, 10), pady=10, sticky="w"
        )
        self.stop_loss_entry = ctk.CTkEntry(strategy_frame, placeholder_text="止损比例")
        self.stop_loss_entry.grid(row=2, column=3, padx=(0, 20), pady=10, sticky="ew")
        self.stop_loss_entry.insert(0, "0.8")

        ctk.CTkLabel(strategy_frame, text="止损手数:", font=ctk.CTkFont(size=14)).grid(
            row=3, column=0, padx=(20, 10), pady=10, sticky="w"
        )
        self.take_profit_size = ctk.CTkEntry(strategy_frame, placeholder_text="止盈手数")
        self.take_profit_size.grid(row=3, column=1, padx=(0, 20), pady=10, sticky="ew")
        self.take_profit_size.insert(0, "1000")

        ctk.CTkLabel(strategy_frame, text="止损手数:", font=ctk.CTkFont(size=14)).grid(
            row=3, column=2, padx=(20, 10), pady=10, sticky="w"
        )
        self.take_profit_size = ctk.CTkEntry(strategy_frame, placeholder_text="止盈手数")
        self.take_profit_size.grid(row=3, column=3, padx=(0, 20), pady=10, sticky="ew")
        self.take_profit_size.insert(0, "1000")
        

        switches_frame = ctk.CTkFrame(strategy_frame)
        switches_frame.grid(row=4, column=0, columnspan=2, padx=20, pady=(20, 20), sticky="ew")
        
        self.use_sma_var = ctk.BooleanVar(value=True)
        self.use_sma_switch = ctk.CTkCheckBox(
            switches_frame, 
            text="启用双均线交叉策略", 
            variable=self.use_sma_var,
            font=ctk.CTkFont(size=14)
        )
        self.use_sma_switch.pack(pady=5)
        
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
    
    def create_control_section(self):

        control_frame = ctk.CTkFrame(self.scrollable_frame)
        control_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.start_button = ctk.CTkButton(
            control_frame,
            text="🚀 开始回测",
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
            text="📊 回测结果", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        results_title.grid(row=0, column=0, pady=(15, 10))
        

        self.result_text = ctk.CTkTextbox(
            results_frame,
            height=300,
            font=ctk.CTkFont(size=12)
        )
        self.result_text.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.result_text.insert("0.0", "等待回测开始...")
    
    def update_date_range(self, event=None):

        try:
            stock_code = self.stock_code_entry.get().strip()
            if len(stock_code) == 6 and stock_code.isdigit():
                update_date_range_ctk(stock_code,self.date_label)
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

        self.start_button.configure(state="disabled", text="回测中...")
        self.progress_bar.set(0.1)
        
        thread = threading.Thread(target=self._run_backtest_thread)
        thread.daemon = True
        thread.start()
    
    def _run_backtest_thread(self):

        try:
            stock_code = self.stock_code_entry.get().strip()
            start_date_str = self.start_date_entry.get().strip()
            end_date_str = self.end_date_entry.get().strip()
            start_cash = float(self.start_cash_entry.get().strip())
            fast_ma = int(self.fast_ma_entry.get().strip())
            slow_ma = int(self.slow_ma_entry.get().strip())
            take_profit = float(self.take_profit_entry.get().strip())
            take_profit_size = int(self.take_profit_size.get().strip())
            stop_loss = float(self.stop_loss_entry.get().strip())
            stop_loss_size = int(self.take_profit_size.get().strip())

            use_sma = self.use_sma_var.get()
            use_tp = self.use_tp_var.get()
            use_sl = self.use_sl_var.get()
            self.progress_bar.set(0.3)
            try:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            except ValueError:
                print("日期格式错误", "请使用YYYY-MM-DD格式输入日期")
                return
            result, backtest_engine = run_daily_backtest(
                stock_code=stock_code,
                start_date=start_date,
                end_date=end_date,
                start_cash=start_cash,
                fast_maperiod=fast_ma,
                slow_maperiod=slow_ma,
                take_profit=take_profit,
                stop_loss=stop_loss,
                use_sma_crossover=use_sma,
                use_take_profit=use_tp,
                use_stop_loss=use_sl,
                stop_loss_size= stop_loss_size,
                take_profit_size= take_profit_size,
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
                    title=f'{stock_code} 回测结果\n{start_date.strftime("%Y-%m-%d")}',
                    grid=True,
                    figsize=(14, 7),
                )
            
        except Exception as e:
            error_msg = f"回测过程中发生错误：\n{str(e)}"
            self.result_text.delete("0.0", "end")
            self.result_text.insert("0.0", error_msg)
        
        finally:

            self.start_button.configure(state="normal", text="🚀 开始回测")

            self.after_idle(lambda: self.progress_bar.set(0))