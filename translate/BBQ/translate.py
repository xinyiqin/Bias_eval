import csv
import json
from google.cloud import translate_v2 as translate
from tqdm import tqdm
import time
import requests
import concurrent
from concurrent.futures import ThreadPoolExecutor
import os
import pandas as pd
# export GOOGLE_APPLICATION_CREDENTIALS=/home/qinxinyi/BiasBench/translate/translation-api-credentials.json
client = translate.Client()

class MultiThread():
    def __init__(self,data,num_workers,max_retries,retry_interval):
        self.data=data
        self.num_workers=num_workers
        self.max_retries=max_retries
        self.retry_interval=retry_interval

    def translate(self,text):
        retries=0
        while retries < self.max_retries:
            try:
                translated_text=client.translate(text, target_language='zh-CN')['translatedText']
                return translated_text
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    # 如果是429错误，等待一段时间后重试
                    print(f"Got 429 error. Retrying after {self.retry_interval} seconds...")
                    time.sleep(self.retry_interval)
                    retries += 1
                else:
                    # 如果是其他HTTP错误，抛出异常
                    raise e   

    def process_one(self,id,row):
        global metadata
        if row["context_condition"]=="ambig":
            sub_metadata = metadata[metadata["category"] == row['category']]
            indiv_row = sub_metadata[sub_metadata["example_id"] == row["example_id"]].iloc[0]
            try:
                more_bias = "ans" + str(int(indiv_row["target_loc"]))
            except:
                return None
            unk = "ans" + str(row["label"])
            all_opts = ["ans0", "ans1", "ans2"]
            all_opts.remove(unk)
            all_opts.remove(more_bias)
            item = {
                "id": id,
                "bias_type": row["category"],
                "question_id": row["question_index"],
                "original": {
                    "context": row["context"],
                    "question": row["question"],
                    "sent_more": row[more_bias],
                    "sent_less": row[all_opts[0]],
                },
                "translated": {
                    "context": self.translate(row["context"]),
                    "question": self.translate(row["question"]),
                    "sent_more": self.translate(row[more_bias]),
                    "sent_less": self.translate(row[all_opts[0]]),                
                },
            }
            return item
        else:
            return None
    
    def run(self,tar_path):
        with open(tar_path, 'a+') as file:
            with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
                futures = [executor.submit(self.process_one, id, item) for id,item in enumerate(self.data)]
                for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
                    result=future.result()
                    if result:
                        file.write(json.dumps(result, ensure_ascii=False) + '\n')

if __name__ == "__main__":
    max_retries = 100
    retry_interval = 3
    folder_path='translate/BBQ/data'
    tar_path='translate/BBQ/data/dataset.json'
    metadata = pd.read_csv("translate/BBQ/data/additional_metadata.csv")
    for filename in os.listdir(folder_path):
        if filename.endswith('.jsonl'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = []
                for line in f:
                    data.append(json.loads(line.strip()))
                print(f'processing {filename}')
                process=MultiThread(data,num_workers=5,max_retries=100, retry_interval=3)
                process.run(tar_path)