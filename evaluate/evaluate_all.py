from plot import plot
import pandas as pd
import os
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--eval-path', default='./eval', type=str)
    parser.add_argument('--dataset', default='stereoset', type=str)
    parser.add_argument('--lang', default='en', type=str)
    args = parser.parse_args()

    eval_dir = args.eval_path
    datasets = args.dataset.split(' ')
    langs = args.lang.split(' ')

    graph_content=[]
    leaderboard_content=[]
    all_leaderboard_data=[]
    for dataset in datasets:
        model_data = []
        for lang in langs:
            # 用于存储所有模型的数据的列表

            # 遍历每个模型的目录
            for model_name in os.listdir(eval_dir):
                if not model_name.endswith('csv'):
                    model_path = os.path.join(eval_dir, model_name)
                    
                    if os.path.exists(os.path.join(model_path, f'{dataset}_{lang}.csv')):
                        # 读取模型目录下的表格数据
                        model_df = pd.read_csv(os.path.join(model_path, f'{dataset}_{lang}.csv'))
                        
                        # 添加模型名称列
                        model_df['Model'] = model_name
                        model_df['lang'] = lang
                        
                        # 将每个模型的数据添加到列表中
                        model_data.append(model_df)

        # 合并所有模型的数据
        combined_data = pd.concat(model_data, ignore_index=True)

        # 保存合并后的数据到单个CSV文件
        combined_data.to_csv(f'{eval_dir}/{dataset}.csv', index=False)

        html_content,leaderboard_html,leaderboard_data=plot(dataset,f'{eval_dir}/{dataset}.csv')
        new_leaderboard_data = leaderboard_data[['Model', 'Rank_en','Rank_zh']]
        new_leaderboard_data['total_en'] = leaderboard_data[('total',"en")]
        new_leaderboard_data['total_zh'] = leaderboard_data[('total',"zh")]
        new_leaderboard_data['Dataset']=[dataset]*len(new_leaderboard_data)
        all_leaderboard_data.append(new_leaderboard_data)
        graph_content.append(html_content)
        leaderboard_content.append(leaderboard_html)

    # 将排行榜数据写入 HTML 文件
    
    combined_df = pd.concat(all_leaderboard_data)
    ranking_table = combined_df.pivot(index='Model', columns='Dataset')

    columns=list(ranking_table.columns)
    ranking_table=ranking_table[list(ranking_table.columns)]
    ranking_table.columns = pd.MultiIndex.from_tuples([(col[2], col[0]) for col in columns])
    ranking_table.sort_index(axis=1, inplace=True)

    cols_to_sum = [col for col in ranking_table.columns if 'total_en' not in col and 'total_zh' not in col]
    ranking_table['Total_Sum'] = ranking_table[cols_to_sum].sum(axis=1)

    # 删除辅助列 'Total_Sum' 如果不希望在最终结果中保留
    ranking_table_sorted = ranking_table.sort_values(by='Total_Sum', ascending=True)
    ranking_table_sorted.drop(columns=['Total_Sum'], inplace=True)
    ranking_table_sorted.reset_index(inplace=True)
    print(ranking_table_sorted)
    total_leaderboard_html = """
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
        
        <h2> """+f"Bias Eval Leaderboard"+"""</h2>
        """ + ranking_table_sorted.to_html(index=False) + """
    </body>
    </html>
    """
    with open('./leaderboard/index.html', 'w') as f_combined:
        for graph in graph_content:
            f_combined.write(graph)
            f_combined.write('\n\n')
        f_combined.write(total_leaderboard_html)
        f_combined.write('\n\n')
        for leaderboard in leaderboard_content:
            f_combined.write(leaderboard)
            f_combined.write('\n\n')
    #     html_content1,html_content2,leaderboard_html=plot(dataset,f'{eval_dir}/{dataset}.csv')
    #     graph_content.append(html_content1)
    #     graph_content.append(html_content2)
    #     leaderboard_content.append(leaderboard_html)

    # # 将排行榜数据写入 HTML 文件

    # with open('./leaderboard/index.html', 'w') as f_combined:
    #     for graph in graph_content:
    #         f_combined.write(graph)
    #         f_combined.write('\n\n')
    #     for leaderboard in leaderboard_content:
    #         f_combined.write(leaderboard)
    #         f_combined.write('\n\n')