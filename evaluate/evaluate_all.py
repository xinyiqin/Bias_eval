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
            
        html_content,leaderboard_html=plot(dataset,f'{eval_dir}/{dataset}.csv')
        graph_content.append(html_content)
        leaderboard_content.append(leaderboard_html)

    # 将排行榜数据写入 HTML 文件

    with open('./leaderboard/index.html', 'w') as f_combined:
        for graph in graph_content:
            f_combined.write(graph)
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