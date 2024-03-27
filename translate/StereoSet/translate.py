import json
from tqdm import tqdm
import time
import requests
from google.cloud import translate_v2 as translate
import concurrent
from concurrent.futures import ThreadPoolExecutor
import os
# export GOOGLE_APPLICATION_CREDENTIALS=/home/qinxinyi/translate/translation-api-credentials.json
# 创建一个 Translate 客户端
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
                
    def process_one(self,index,num_existing_result,item):
        if index >= num_existing_result:
            translated_context=self.translate(item["context"])
            item['translated_context']=translated_context
            for sentence in item["sentences"]:
                translated_text=self.translate(sentence["sentence"])
                sentence["translated_sentence"] = translated_text   
            return item
        else:
            return None
    
    def run(self,tar_path,num_existing_result):
        with open(tar_path, 'a+') as file:
            with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
                futures = [executor.submit(self.process_one, index, num_existing_result, item) for index,item in enumerate(self.data["data"]["intersentence"])]
                for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
                    result=future.result()
                    file.write(json.dumps(result, ensure_ascii=False) + '\n')

if __name__ == "__main__":
    max_retries = 100
    retry_interval = 3
    sou_path='/home/qinxinyi/translate/StereoSet/data/dev.json'
    tar_path='/home/qinxinyi/translate/StereoSet/data/translated_dev.json'
    num_existing_result = 0  # if the result file already exists, skip the test cases that have been tested.
    if os.path.exists(tar_path):
        with open(tar_path) as f:
            for line in f:
                num_existing_result += 1
    with open(sou_path, 'r') as file:
        data = json.load(file)
        process=MultiThread(data,num_workers=5,max_retries=100, retry_interval=3)
        process.run(tar_path,num_existing_result)