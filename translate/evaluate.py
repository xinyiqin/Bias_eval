import torch
from sentence_transformers import SentenceTransformer

# 检查GPU是否可用
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 加载模型，并将其移动到GPU上
model = SentenceTransformer('intfloat/multilingual-e5-large-instruct')
model.to(device)

data = ['A homely recipe for pumpkins','A homely recipe for pumpkins','南瓜的家常做法']
translated_data=['南瓜的家常做法','南瓜怎么种植','南瓜的家常做法']

# 将数据转换为PyTorch张量，并将其移动到GPU上
data_tensors = model.encode(data, convert_to_tensor=True, device=device)
translated_tensors = model.encode(translated_data, convert_to_tensor=True, device=device)

# 对于计算相似度，使用PyTorch张量操作，这将利用GPU加速
sims = torch.sum(data_tensors * translated_tensors, dim=1)
print(sims.cpu().tolist())  # 将结果移回CPU并打印
