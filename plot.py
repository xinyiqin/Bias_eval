import pandas as pd
import numpy as np
import plotly.graph_objects as go

def plot(dataset,data_path):
    # 从CSV文件中读取数据
    data = pd.read_csv(data_path)

    # 提取模型名称
    models = data['Model'].tolist()
    data.set_index('Model', inplace=True)

    data = data[['total'] + [col for col in data.columns if col != 'total']]

    # 提取特征和数值
    features = data.columns
    values = data.values

    # 设置雷达图的参数
    angles = np.linspace(0, 360, len(features), endpoint=False).tolist()
    fig = go.Figure()
    print(len(values))
    colors = [
        '#9966ff', '#ffce56', '#ff6384', '#36a2eb',
        '#3cb371', '#6ad79d', '#7a73d9', '#d973bf',
        '#207fec', '#d54747', '#ee9822', '#20eeb4',
        '#FF6666','#99CC66','#336633', '#2c8c31',
    ]

    for i in range(len(values)):
        stats_data = values[i].tolist()
        fig.add_trace(go.Scatterpolar(
            r=stats_data,
            theta=angles,
            mode='lines+markers',
            name=models[i],
            line=dict(color=colors[i], width=3),  # 设置线条颜色
            marker=dict(color=colors[i], symbol='circle', size=8, line=dict(color='white', width=1.5))  # 设置标记颜色
        ))

    # 更新布局
    fig.update_layout(
        title=f'{dataset.capitalize()} Leaderboard',
        polar=dict(
            radialaxis=dict(
                visible=False,
                range=[0, 100]
            ),
            angularaxis=dict(
                tickmode='array',
                tickvals=angles,
                ticktext=features,
                showline=True,
                linewidth=8,
                direction='clockwise'
            )
        ),
        showlegend=True
    )

    html_content = fig.to_html(include_plotlyjs='cdn')
    # leaderboard_html = leaderboard_data.to_html()

    # 生成排行榜的HTML内容并应用样式
    # 创建排行榜数据
    leaderboard_data = pd.read_csv(data_path)
    print(leaderboard_data)
    leaderboard_data['Rank'] = leaderboard_data["total"].rank(ascending=False).astype(int)
    leaderboard_data.set_index('Rank', inplace=True)
    leaderboard_data.sort_index(inplace=True)

    leaderboard_data = leaderboard_data.round(2)
    # 调整列的顺序，将“Total”列移动到第一列
    columns = leaderboard_data.columns.tolist()
    columns.insert(1, columns.pop(columns.index('total')))
    leaderboard_data = leaderboard_data[columns]
    print(leaderboard_data)
    leaderboard_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            /* 添加样式 */
            table {
                font-family: Arial, sans-serif;
                border-collapse: collapse;
                width: 100%;
            }

            th, td {
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }

            th {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>
        
        <h2> """+f"{dataset.capitalize()} Leaderboard"+"""</h2>
        """ + leaderboard_data.to_html() + """
    </body>
    </html>
    """
    return html_content,leaderboard_html

