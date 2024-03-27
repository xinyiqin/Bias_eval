import json

# 读取数据集文件
dataset=[]
with open('/home/qinxinyi/translate/StereoSet/data/translated_dev.json', 'r', encoding='utf-8') as f:
    for line in f:
        if 'context' in line:
            dataset.append(json.loads(line))
with open('/home/qinxinyi/translate/StereoSet/data/translated_test.json', 'r', encoding='utf-8') as f:
    for line in f:
        if 'context' in line:
            dataset.append(json.loads(line))

new_dataset=[]
# 提取每条数据的 context 和 sentences
from tqdm import tqdm
for id,data in tqdm(enumerate(dataset),total=len(dataset)):
    # print(data)
    context = data['context']
    sentences = data['sentences']
    
    # 构建 original 数据结构
    original_data = {
        "context": context,
        "sentences": [{"sentence": s['sentence'], "label": s['gold_label']} for s in sentences]
    }
    
    # 构建 translated 数据结构
    translated_data = {
        "context": data['translated_context'],
        "sentences": [{"sentence": s['translated_sentence'], "label": s['gold_label']} for s in data['sentences']]
    }
    
    # 添加到新数据集中
    new_data = {"id":id,"bias_type":data['bias_type'],"target":data['target'],"original": original_data, "translated": translated_data}
    new_dataset.append(new_data)

# 将新数据集保存到新的 JSON 文件中
with open('/home/qinxinyi/translate/StereoSet/data/reformat_dataset.json', 'w', encoding='utf-8') as f:
    for line in new_dataset:
        f.write(json.dumps(line,ensure_ascii=False)+'\n')
