import plotly.graph_objects as go

class RenderUtil:
    def __init__(self):
        super(RenderUtil, self).__init__()

    def draw_k_line(self, df):
        df['MA5'] = df['close'].rolling(window=5).mean()
        df['MA20'] = df['close'].rolling(window=20).mean()
        df['MA60'] = df['close'].rolling(window=60).mean()

        fig = go.Figure()

        fig.add_trace(go.Candlestick(
            x=df['date'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='股价',
            increasing_line_color='red',
            decreasing_line_color='green',
            increasing_fillcolor='red',
            decreasing_fillcolor='green'
        ))

        # 🔥 添加移动平均线
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['MA5'],
            mode='lines',
            name='MA5',
            line=dict(color='blue', width=1),
            hovertemplate='MA5: ¥%{y:.2f}<extra></extra>'
        ))

        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['MA20'],
            mode='lines',
            name='MA20',
            line=dict(color='orange', width=1.5),
            hovertemplate='MA20: ¥%{y:.2f}<extra></extra>'
        ))

        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['MA60'],
            mode='lines',
            name='MA60',
            line=dict(color='purple', width=2),
            hovertemplate='MA60: ¥%{y:.2f}<extra></extra>'
        ))

        fig.update_layout(
            title='k线图',
            yaxis_title='价格 (元)',
            xaxis_title='日期',
            width=1200,
            height=600,
            xaxis_rangeslider_visible=False,
            legend=dict(
                x=0.01,
                y=0.99,
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='rgba(0,0,0,0.2)',
                borderwidth=1
            )
        )

        fig.show()


        return fig
