import pandas as pd
import numpy as np
import plotly.graph_objects as go

def plot(dataset,data_path):
    # 从CSV文件中读取数据
    data = pd.read_csv(data_path)
    print(dataset)
    print(data)
    data = data[['total'] + [col for col in data.columns if col != 'total']]
    data = data[['lang'] + [col for col in data.columns if col != 'lang']]
    models=data['Model'].unique().tolist()
    data.set_index('Model', inplace=True)
    features = data.columns.tolist()[1:]
    en_values = data[data['lang']=='en'].values[:, 1:]
    zh_values = data[data['lang']=='zh'].values[:, 1:]
    data.reset_index()
    # print(features)
    # 设置雷达图的参数
    angles = np.linspace(0, 360, len(features), endpoint=False).tolist()
    fig = go.Figure()

    colors = [
        '#9966ff', '#ffce56', '#ff6384', '#36a2eb',
        '#3cb371', '#6ad79d', '#7a73d9', '#d973bf',
        '#207fec', '#d54747', '#ee9822', '#20eeb4',
        '#FF6666','#99CC66','#336633', '#2c8c31',
    ]

    for i in range(len(models)):
        en_stats_data = en_values[i].tolist()
        fig.add_trace(go.Scatterpolar(
            r=en_stats_data,
            theta=angles,
            mode='lines+markers',
            name=f'{models[i]} - English',
            legendgroup=models[i],
            line=dict(color=colors[i], width=3),  # 设置线条颜色
            marker=dict(color=colors[i], symbol='circle', size=8, line=dict(color='white', width=1.5)),  # 设置标记颜色
            hovertemplate=f'{models[i]} - English<br>' + '<br>'.join([f'{feature}: %{en_stats_data[i]}' for i, feature in enumerate(features)]),
        ))
        zh_stats_data = zh_values[i].tolist()
        fig.add_trace(go.Scatterpolar(
            r=zh_stats_data,
            theta=angles,
            mode='lines+markers',
            name=f'{models[i]} - Chinese',
            legendgroup=models[i],
            line=dict(color=colors[i], width=3, dash='dash'),  # 设置线条颜色
            marker=dict(color=colors[i], symbol='circle', size=8, line=dict(color='white', width=1.5)),  # 设置标记颜色
            customdata=[f'{models[i]} - Chinese'] * len(en_stats_data),  # 保存自定义数据
            hovertemplate=f'{models[i]} - Chinese<br>' + '<br>'.join([f'{feature}: %{zh_stats_data[i]}' for i, feature in enumerate(features)]),
        ))

        # 更新布局
    fig.update_layout(
        title=f"{dataset.capitalize()} Leaderboard",
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

    # 添加JavaScript代码
    fig.update_layout(
        updatemenus=[
            {
                "buttons": [
                    {
                        "args": [None, {"frame": {"duration": 500, "redraw": True}, "fromcurrent": True}],
                        "label": "Play",
                        "method": "animate",
                    }
                ],
                "showactive": False,
                "type": "buttons",
            }
        ]
    )
    html_content = fig.to_html(include_plotlyjs='cdn')
    # leaderboard_html = leaderboard_data.to_html()

    # 生成排行榜的HTML内容并应用样式
    # 创建排行榜数据
    leaderboard_data = pd.read_csv(data_path)
    leaderboard_data['Rank_en']=leaderboard_data['Model']
    leaderboard_data['Rank_zh']=leaderboard_data['Model']
    leaderboard_data = leaderboard_data.pivot(index=["Model",'Rank_en','Rank_zh'], columns="lang")

    columns=list(leaderboard_data.columns)
    columns.insert(0, columns.pop(columns.index(('total','zh'))))
    columns.insert(0, columns.pop(columns.index(('total','en'))))
    leaderboard_data=leaderboard_data[columns]
    leaderboard_data.columns = pd.MultiIndex.from_tuples([(col[0], col[1]) for col in columns])

    leaderboard_data.reset_index(inplace=True)
    leaderboard_data['Rank_en'] = leaderboard_data[('total',"en")].rank(ascending=False).astype(int)
    leaderboard_data['Rank_zh'] = leaderboard_data[('total',"zh")].rank(ascending=False).astype(int)
    leaderboard_data = leaderboard_data.sort_values('Rank_en')
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
        """ + leaderboard_data.to_html(index=False) + """
    </body>
    </html>
    """
    return html_content,leaderboard_html

