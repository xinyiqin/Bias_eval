
import json
from tqdm import tqdm
import random
import pandas as pd
import openai
import json
from tqdm import tqdm
import argparse
# from prompts import prompt_templates
import os
import time
import concurrent
from concurrent.futures import ThreadPoolExecutor
import threading
from generator import Generator
from generator_open_source import OpenGenerator
import sensenova
import google.generativeai as genai


def generate_one(num_existing_result,idx,row,lang,dataset,prompt_map,answer_num,args):
    if str(row['id'])+row['bias_type'] not in num_existing_result:
        try:
            user_prompt=prompt_map[idx]['prompt']
        except:
            user_prompt=None
        if not user_prompt:   
            if lang=='en':
                data=row['original'] if dataset!='cbbq' else row['translated']
            elif lang=='zh':
                data=row['translated'] if dataset!='cbbq' else row['original']
                for name,sentence in data.items():
                    if not sentence.endswith('。') and not sentence.endswith('？'):
                        data[name]=sentence+'。'
            else:
                print('invalid lang.')
            if lang=='en':
                question=f"{data['context']+ ' ' +data['question']}"
            elif lang=='zh':
                question=f"{data['context']+data['question']}"
            
            prompt = {"id":row["id"],
                            "dataset":dataset,
                                "bias_type":row["bias_type"],
                                "lang":lang,
                                "prompt":question,
                            }
            retry=0
            while retry<args.retry_times:
                try:
                    if 'gpt'in model:
                        response = generator.chat_completion(user_prompt=question,n=answer_num,max_tokens=args.max_new_tokens,temperature=0.7)
                        time.sleep(2)
                    # generate n results for one question
                    else:
                        response=[]
                        for _ in range(answer_num):
                            cnt=0
                            while cnt<=5:
                                try:
                                    response.append(generator.chat_completion(user_prompt=question,max_tokens=args.max_new_tokens,temperature=0.7))
                                    time.sleep(1) #sensechat 1 minimax 5
                                    break
                                except genai.types.generation_types.BlockedPromptException as e:
                                    print('gemini block')
                                    break
                                except Exception as e:
                                    print('sleep 2s')
                                    print(str(e))
                                    time.sleep(1) #sensechat 2 minimax 5
                                    cnt+=1
                    assert len(response)==answer_num
                    result = {"id":row["id"],
                                "dataset":dataset,
                                "model":model,
                                "bias_type":row["bias_type"],
                                "lang":lang,
                                "question":question,
                                "response":response,}
                    if model=='sensechat':
                        time.sleep(2)
                    return prompt,result
                except Exception as e:
                    print(str(e))
                    print('sleep 30s...')
                    time.sleep(30)
                    retry+=1
            return prompt,None
        
        else:
            retry=0
            while retry<args.retry_times:
                try:
                    if 'gpt'in model:
                        response = generator.chat_completion(user_prompt,n=answer_num,max_tokens=args.max_new_tokens,temperature=0.7)
                        time.sleep(2)
                    # generate n results for one question
                    else:
                        response=[]
                        for _ in range(answer_num):
                            cnt=0
                            while cnt<=5:
                                try:
                                    response.append(generator.chat_completion(user_prompt,max_tokens=args.max_new_tokens,temperature=0.7))
                                    time.sleep(5) #sensechat 1 minimax 5
                                    break
                                except genai.types.generation_types.BlockedPromptException as e:
                                    print('gemini block')
                                    break
                                except Exception as e:
                                    print('sleep 2s')
                                    print(str(e))
                                    time.sleep(5) #sensechat 2 minimax 5
                                    cnt+=1
                    assert len(response)==answer_num
                    result = {"id":row["id"],
                            "dataset":dataset,
                                "model":model,
                                "bias_type":row["bias_type"],
                                "lang":lang,
                                "question":prompt_map[idx]["prompt"],
                                "response":response,
                                }
                    return None,result
                except Exception as e:
                    print(str(e))
                    print('sleep 30s...')
                    time.sleep(30)
                    retry+=1
            return None,None
    else:
        return None,num_existing_result[str(row['id'])+row['bias_type']]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-path', default='./data', type=str)
    parser.add_argument('--output-path', default='./expr', type=str)
    parser.add_argument('--prompt-path', default='./expr/prompt', type=str)
    # parser.add_argument('--word', default='accurate', type=str)
    parser.add_argument('--model', default='gpt-3.5', type=str)
    parser.add_argument('--limit', default=None, type=int)
    parser.add_argument('--dataset', default='stereoset', type=str)
    parser.add_argument('--lang', default='en', type=str)
    parser.add_argument('--num_workers', default=32, type=int)
    parser.add_argument('--retry_times', default=1, type=int)
    parser.add_argument('--max_new_tokens', default=100, type=int)
    parser.add_argument('--answer_num', default=1, type=int)
    args = parser.parse_args()

    limit=args.limit
    num_workers = args.num_workers
    data_dir = args.data_path
    output_dir = args.output_path
    # word = args.word
    prompt_dir = args.prompt_path
    model = args.model
    dataset = args.dataset
    lang = args.lang
    answer_num=args.answer_num

    if any([i in model for i in ['qwen','openbuddy','alpaca','llama','internlm','baichuan','chatglm']]):
        generator=OpenGenerator(model)
    else:
        generator=Generator(model)

    if not os.path.exists(f"{output_dir}/{model}"):
        os.makedirs(f"{output_dir}/{model}")
    prompt_path=f'{prompt_dir}/{dataset}_{lang}_qa.json'
    output_path=f"{output_dir}/{model}/{dataset}_{lang}_qa.json"

    with open(f'{data_dir}/{dataset}.json', 'r', encoding='utf-8') as f:
        data=[]
        for line in f:
            data.append(json.loads(line))
        if limit: 
            data = data[:limit]
        print(f'loading dataset {dataset} successfully.')

    prompt_map=[]
    if os.path.exists(prompt_path):
        with open(prompt_path, "r") as prompt_f:
            for line in prompt_f:
                prompt_map.append(json.loads(line))

    if os.path.exists(output_path):
        new_output_path=f"{output_dir}/{model}/{dataset}_{lang}_2.json"
        if os.path.exists(new_output_path):
            os.remove(output_path)
            os.rename(new_output_path, output_path)
            output_place=new_output_path
        else:
            output_place=new_output_path
    else:
        output_place=output_path

    num_existing_result = {}
    if os.path.exists(output_path):
        with open(output_path,"r") as output_f:
            for line in output_f:
                line=json.loads(line)
                num_existing_result[str(line['id'])+line['bias_type']]=line

    def write_results():
        global futures, write_index
        with tqdm(total=len(futures), desc="Writing results") as pbar:
            while write_index < len(futures):
                future = futures[write_index]
                if future.done():
                    prompt, result = future.result()
                    with open(prompt_path, "a+") as prompt_f, open(output_place, "a+") as output_f:
                        if result:
                            json.dump(result, output_f, ensure_ascii=False)
                            output_f.write("\n")
                        if prompt:
                            json.dump(prompt, prompt_f, ensure_ascii=False)
                            prompt_f.write("\n")
                    write_index += 1
                    pbar.update(1)

    print(f'Inference {model}...')
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(generate_one,num_existing_result,index,row,lang,dataset,prompt_map,answer_num,args) for index, row in enumerate(data)]
        write_index=0
        write_thread = threading.Thread(target=write_results)
        write_thread.start()
        for _ in tqdm(concurrent.futures.as_completed(futures), total=len(futures),desc="Generate results"):
            pass
    
    write_thread.join()

    if output_place==f"{output_dir}/{model}/{dataset}_{lang}_2.json":
        os.remove(output_path)
        os.rename(new_output_path, output_path)