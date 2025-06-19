import customtkinter as ctk
from PIL import Image
import webbrowser
import os
import subprocess
import sys


class NewHomePage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # GitHub项目链接 - 请替换为您的实际GitHub链接
        self.github_url = "https://github.com/yourusername/Quantitative_Trading"
        # 项目文档路径 - 请替换为您的实际文档路径
        self.doc_path = "项目介绍.docx"

        self.create_home_content()

    def create_home_content(self):
        """创建主页内容"""
        # 顶部标题
        title_label = ctk.CTkLabel(
            self,
            text="🏠 神秘股市量化交易系统",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=("gray10", "gray90")
        )
        title_label.grid(row=0, column=0, pady=(20, 10))

        # 可滚动的主要内容区域
        self.scrollable_frame = ctk.CTkScrollableFrame(self, corner_radius=15)
        self.scrollable_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # 创建各个部分
        self.create_welcome_section()
        self.create_action_buttons()
        self.create_team_section()
        self.create_features_section()
        self.create_tech_stack_section()
        self.create_usage_guide()

    def create_welcome_section(self):
        """创建欢迎部分"""
        welcome_frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=15)
        welcome_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ew")
        welcome_frame.grid_columnconfigure(0, weight=1)

        # 项目logo或图标区域
        icon_label = ctk.CTkLabel(
            welcome_frame,
            text="📊💰📈",
            font=ctk.CTkFont(size=48)
        )
        icon_label.grid(row=0, column=0, pady=(25, 15))

        # 项目描述
        desc_label = ctk.CTkLabel(
            welcome_frame,
            text="专业的Python股票量化交易回测平台\n支持多种策略回测，提供详细的数据分析和可视化功能",
            font=ctk.CTkFont(size=16),
            text_color=("gray20", "gray80"),
            justify="center"
        )
        desc_label.grid(row=1, column=0, pady=(0, 25))

    def create_action_buttons(self):
        """创建操作按钮部分"""
        buttons_frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=15)
        buttons_frame.grid(row=1, column=0, padx=15, pady=15, sticky="ew")
        buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)

        buttons_title = ctk.CTkLabel(
            buttons_frame,
            text="🔗 项目资源",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#1f6aa5", "#4a9eff")
        )
        buttons_title.grid(row=0, column=0, columnspan=3, pady=(20, 20))

        # GitHub按钮
        github_btn = ctk.CTkButton(
            buttons_frame,
            text="🚀 访问 GitHub",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            corner_radius=12,
            fg_color=("#2d2d2d", "#1a1a1a"),
            hover_color=("#404040", "#333333"),
            command=self.open_github
        )
        github_btn.grid(row=1, column=0, padx=15, pady=15, sticky="ew")

        # 项目文档按钮
        doc_btn = ctk.CTkButton(
            buttons_frame,
            text="📄 项目文档",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            corner_radius=12,
            fg_color=("#1f6aa5", "#4a9eff"),
            hover_color=("#1e5f99", "#3a8cef"),
            command=self.open_documentation
        )
        doc_btn.grid(row=1, column=1, padx=15, pady=15, sticky="ew")

        # 使用帮助按钮
        help_btn = ctk.CTkButton(
            buttons_frame,
            text="❓ 使用帮助",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            corner_radius=12,
            fg_color=("#d97706", "#f59e0b"),
            hover_color=("#c2640c", "#e19009"),
            command=self.show_help
        )
        help_btn.grid(row=1, column=2, padx=15, pady=15, sticky="ew")

    def create_team_section(self):
        """创建团队介绍部分"""
        team_frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=15)
        team_frame.grid(row=2, column=0, padx=15, pady=15, sticky="ew")
        team_frame.grid_columnconfigure(0, weight=1)

        team_title = ctk.CTkLabel(
            team_frame,
            text="👥 开发团队",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=("#1f6aa5", "#4a9eff")
        )
        team_title.grid(row=0, column=0, pady=(20, 15))

        team_desc = ctk.CTkLabel(
            team_frame,
            text="由四位热爱金融科技的开发者共同打造\n我们致力于为投资者提供专业、易用的量化交易工具",
            font=ctk.CTkFont(size=14),
            text_color=("gray30", "gray70"),
            justify="center"
        )
        team_desc.grid(row=1, column=0, pady=(0, 20))

        # 团队成员展示区域
        members_container = ctk.CTkFrame(team_frame, fg_color="transparent")
        members_container.grid(row=2, column=0, pady=(0, 20))
        members_container.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # 团队成员卡片
        for i in range(4):
            member_card = ctk.CTkFrame(members_container, width=120, height=80, corner_radius=10)
            member_card.grid(row=0, column=i, padx=10, pady=10)
            member_card.grid_propagate(False)
            
            member_icon = ctk.CTkLabel(member_card, text="👤", font=ctk.CTkFont(size=20))
            member_icon.pack(pady=(10, 5))
            
            member_label = ctk.CTkLabel(member_card, text=f"成员 {i+1}", font=ctk.CTkFont(size=12))
            member_label.pack()

    def create_features_section(self):
        """创建功能特性部分"""
        features_frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=15)
        features_frame.grid(row=3, column=0, padx=15, pady=15, sticky="ew")
        features_frame.grid_columnconfigure((0, 1), weight=1)

        features_title = ctk.CTkLabel(
            features_frame,
            text="⚡ 核心功能",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=("#1f6aa5", "#4a9eff")
        )
        features_title.grid(row=0, column=0, columnspan=2, pady=(20, 20))

        # 日K回测功能
        daily_card = ctk.CTkFrame(features_frame, corner_radius=12)
        daily_card.grid(row=1, column=0, padx=15, pady=15, sticky="nsew")

        daily_icon = ctk.CTkLabel(daily_card, text="📈", font=ctk.CTkFont(size=32))
        daily_icon.pack(pady=(15, 10))

        daily_title = ctk.CTkLabel(
            daily_card,
            text="日K线回测",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        daily_title.pack(pady=(0, 10))

        daily_features = ctk.CTkLabel(
            daily_card,
            text="• 双均线交叉策略\n• 智能止盈止损\n• 详细回测报告\n• 可视化图表展示\n• 多参数优化",
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        daily_features.pack(pady=(0, 15))

        # 分时回测功能
        tick_card = ctk.CTkFrame(features_frame, corner_radius=12)
        tick_card.grid(row=1, column=1, padx=15, pady=15, sticky="nsew")

        tick_icon = ctk.CTkLabel(tick_card, text="⏰", font=ctk.CTkFont(size=32))
        tick_icon.pack(pady=(15, 10))

        tick_title = ctk.CTkLabel(
            tick_card,
            text="分时数据回测",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        tick_title.pack(pady=(0, 10))

        tick_features = ctk.CTkLabel(
            tick_card,
            text="• 分钟级别数据\n• 价格成交量指标\n• 高频交易策略\n• 实时信号捕捉\n• 超短线策略",
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        tick_features.pack(pady=(0, 15))

    def create_tech_stack_section(self):
        """创建技术栈部分"""
        tech_frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=15)
        tech_frame.grid(row=4, column=0, padx=15, pady=15, sticky="ew")

        tech_title = ctk.CTkLabel(
            tech_frame,
            text="🛠️ 技术栈",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#1f6aa5", "#4a9eff")
        )
        tech_title.grid(row=0, column=0, pady=(20, 15))

        tech_list = ctk.CTkLabel(
            tech_frame,
            text="Python • Tkinter • CustomTkinter • Backtrader • Pandas • NumPy • Akshare • Matplotlib",
            font=ctk.CTkFont(size=13),
            text_color=("gray30", "gray70"),
            justify="center"
        )
        tech_list.grid(row=1, column=0, pady=(0, 20))



    def create_usage_guide(self):
        """创建使用指南部分"""
        guide_frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=15)
        guide_frame.grid(row=5, column=0, padx=15, pady=15, sticky="ew")

        guide_title = ctk.CTkLabel(
            guide_frame,
            text="🚀 快速开始",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#1f6aa5", "#4a9eff")
        )
        guide_title.grid(row=0, column=0, pady=(20, 15))

        steps = [
            "1️⃣ 点击左侧菜单选择回测类型（日K线 或 分时数据）",
            "2️⃣ 输入股票代码（如：000001）和策略参数",
            "3️⃣ 设置回测时间范围和资金配置",
            "4️⃣ 点击开始回测按钮执行策略",
            "5️⃣ 查看详细的回测结果报告和图表分析"
        ]

        for i, step in enumerate(steps):
            step_label = ctk.CTkLabel(
                guide_frame,
                text=step,
                font=ctk.CTkFont(size=13),
                anchor="w",
            justify="left"
            )
            step_label.grid(row=i+1, column=0, pady=5, padx=20, sticky="w")

        # 底部提示
        tip_label = ctk.CTkLabel(
            guide_frame,
            text="💡 提示：建议先从日K线回测开始体验系统功能",
            font=ctk.CTkFont(size=12),
            text_color=("#d97706", "#f59e0b"),
            justify="center"
        )
        tip_label.grid(row=len(steps)+1, column=0, pady=(15, 20))

    def open_github(self):
        """打开GitHub链接"""
        try:
            webbrowser.open(self.github_url)
        except Exception as e:
            self.show_error_dialog("GitHub链接", f"无法打开GitHub链接：{str(e)}")

    def open_documentation(self):
        """打开项目文档"""
        try:
            if os.path.exists(self.doc_path):
                if sys.platform.startswith('win'):
                    os.startfile(self.doc_path)
                elif sys.platform.startswith('darwin'):  # macOS
                    subprocess.call(['open', self.doc_path])
                else:  # Linux
                    subprocess.call(['xdg-open', self.doc_path])
            else:
                self.show_error_dialog("项目文档", f"文档文件不存在：{self.doc_path}\n请确认文件路径是否正确")
        except Exception as e:
            self.show_error_dialog("项目文档", f"无法打开文档文件：{str(e)}")

    def show_help(self):
        """显示帮助信息"""
        help_window = ctk.CTkToplevel(self)
        help_window.title("使用帮助")
        help_window.geometry("600x400")
        help_window.transient(self)
        help_window.grab_set()

        # 帮助内容
        help_text = """
📖 系统使用帮助

🎯 系统概述：
本系统是专业的股票量化交易回测平台，支持多种策略回测和数据分析。

📈 日K线回测：
• 适用于中长期策略回测
• 支持双均线交叉策略
• 可设置止盈止损参数
• 提供详细的回测报告

⏰ 分时回测：
• 适用于短期和超短期策略
• 基于分钟级数据
• 支持价格和成交量指标
• 高频交易策略优化

💡 使用技巧：
1. 选择合适的股票代码进行回测
2. 根据策略类型调整参数设置
3. 合理设置回测时间范围
4. 注意风险控制和资金管理

📞 技术支持：
如遇问题请查看项目文档或访问GitHub项目页面
        """

        help_label = ctk.CTkLabel(
            help_window,
            text=help_text,
            font=ctk.CTkFont(size=12),
            justify="left",
            anchor="nw"
        )
        help_label.pack(fill="both", expand=True, padx=20, pady=20)

        close_btn = ctk.CTkButton(
            help_window,
            text="关闭",
            command=help_window.destroy
        )
        close_btn.pack(pady=(0, 20))

    def show_error_dialog(self, title, message):
        """显示错误对话框"""
        error_window = ctk.CTkToplevel(self)
        error_window.title(title)
        error_window.geometry("400x200")
        error_window.transient(self)
        error_window.grab_set()

        error_label = ctk.CTkLabel(
            error_window,
            text=message,
            font=ctk.CTkFont(size=12),
            wraplength=350,
            justify="center"
        )
        error_label.pack(expand=True, padx=20, pady=20)

        ok_btn = ctk.CTkButton(
            error_window,
            text="确定",
            command=error_window.destroy
        )
        ok_btn.pack(pady=(0, 20))