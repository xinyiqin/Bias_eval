import json
from collections import Counter

# 读取 JSON 文件并解析为 Python 对象
def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data=[]
        for line in f:
            data.append(json.loads(line))
    return data

# 统计 bias_type 列中的类别及其数据量
def count_bias_types(json_data):
    bias_types = [entry['bias_type'] for entry in json_data]
    bias_type_counts = Counter(bias_types)
    return bias_type_counts

# 主函数
def main():
    # 替换为你的 JSON 文件路径
    file_paths = ['./data/bbq.json', './data/crowspairs.json','./data/stereoset.json']

    for file_path in file_paths:
        # 加载 JSON 文件
        json_data = load_json_file(file_path)

        # 统计 bias_type 列中的类别及其数据量
        bias_type_counts = count_bias_types(json_data)

        # 打印结果
        print('\n')
        print(f"File: {file_path}")
        for bias_type, count in bias_type_counts.items():
            print(f"{bias_type}: {count}")

if __name__ == "__main__":
    main()
