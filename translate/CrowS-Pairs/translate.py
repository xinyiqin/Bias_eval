import csv
import json
from google.cloud import translate_v2 as translate
from tqdm import tqdm
import time
import requests
import concurrent
from concurrent.futures import ThreadPoolExecutor
import os
# export GOOGLE_APPLICATION_CREDENTIALS=/home/qinxinyi/translate/translation-api-credentials.json
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

    def process_one(self,id,num_existing_result,row):
        if id >= num_existing_result:
            item = {
                "id": id,  # 假设CSV文件中有一个名为index的列存储了每条数据的id
                "bias_type": row["bias_type"],
                "stereo_antistereo": row["stereo_antistereo"],
                "original": {
                    "sent_more": row["sent_more"],
                    "sent_less": row["sent_less"]
                },
                "translated": {
                    "sent_more": self.translate(row["sent_more"]),
                    "sent_less": self.translate(row["sent_less"])
                }
            }
            return item
        else:
            return None
    
    def run(self,tar_path,num_existing_result):
        with open(tar_path, 'a+') as file:
            with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
                futures = [executor.submit(self.process_one, id, num_existing_result, item) for id,item in enumerate(self.data)]
                for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
                    result=future.result()
                    if result:
                        file.write(json.dumps(result, ensure_ascii=False) + '\n')

if __name__ == "__main__":
    max_retries = 100
    retry_interval = 3
    sou_path='/home/qinxinyi/translate/CrowS-Pairs/data/crows_pairs_anonymized.csv'
    tar_path='/home/qinxinyi/translate/CrowS-Pairs/data/dataset.json'
    num_existing_result = 0  # if the result file already exists, skip the test cases that have been tested.
    if os.path.exists(tar_path):
        with open(tar_path) as f:
            for line in f:
                num_existing_result += 1
    with open(sou_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        process=MultiThread(reader,num_workers=5,max_retries=100, retry_interval=3)
        process.run(tar_path,num_existing_result)