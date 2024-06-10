from evaluator import Evaluator
import json
import os
import argparse
import re
from tqdm import tqdm
import concurrent
from concurrent.futures import ThreadPoolExecutor
import threading

def process_one(num_existing_result,row,eval_num):
    if str(row['id'])+row['bias_type'] not in num_existing_result:
        results=evaluator.multi_evaluate(row['question'],row['response'][0],eval_num)
        row['evaluate_results']=results
        # scores=[result['bias_score'] for result in results]
        return row
    else:
        return num_existing_result[str(row['id'])+row['bias_type']]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--expr-path', default='./expr', type=str)
    parser.add_argument('--output-path', default='./qa_eval', type=str)
    parser.add_argument('--evaluator_model', default="gpt-4o-2024-05-13", type=str)
    parser.add_argument('--eval_num', default=3, type=int)
    parser.add_argument('--candidate_model', default='gpt-3.5', type=str)
    parser.add_argument('--dataset', default='cbbq', type=str)
    parser.add_argument('--lang', default='en', type=str)
    parser.add_argument('--limit', default=None, type=int)
    parser.add_argument('--num_workers', default=1, type=int)
    args = parser.parse_args()

    expr_dir = args.expr_path
    eval_dir = args.output_path
    evaluator_model = args.evaluator_model
    model=args.candidate_model
    dataset = args.dataset
    lang = args.lang
    limit = args.limit
    num_workers = args.num_workers
    eval_num=args.eval_num

    evaluator=Evaluator(model=evaluator_model)
    data_path=f"{expr_dir}/{model}/{dataset}_{lang}_qa.json"

    with open(data_path,'r',encoding='utf-8') as f:
        data=[]
        for line in f:
            data.append(json.loads(line))
        if limit: 
            data = data[:limit]
        print(f'loading {model} answer for dataset {dataset} successfully.')

    save_path=f"{eval_dir}/{model}/{dataset}_qa_{lang}.json"
    if not os.path.exists(f"{eval_dir}/{model}"):
        os.makedirs(f"{eval_dir}/{model}")

    if os.path.exists(save_path):
        new_output_path=f"{eval_dir}/{model}/{dataset}_qa_{lang}_2.json"
        if os.path.exists(new_output_path):
            os.remove(save_path)
            os.rename(new_output_path, save_path)
            output_place=new_output_path
        else:
            output_place=new_output_path
    else:
        output_place=save_path

    num_existing_result = {}
    if os.path.exists(save_path):
        with open(save_path,"r") as output_f:
            for line in output_f:
                line=json.loads(line)
                num_existing_result[str(line['id'])+line['bias_type']]=line

    def write_results():
        global futures, write_index
        with tqdm(total=len(futures), desc="Writing results") as pbar:
            while write_index < len(futures):
                future = futures[write_index]
                if future.done():
                    result = future.result()
                    with open(output_place, "a+") as output_f:
                        if result:
                            json.dump(result, output_f, ensure_ascii=False)
                            output_f.write("\n")
                    write_index += 1
                    pbar.update(1)

    print(f'Inference {model}...')
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(process_one,num_existing_result,row,eval_num) for row in tqdm(data)]
        write_index=0
        write_thread = threading.Thread(target=write_results)
        write_thread.start()
        for _ in tqdm(concurrent.futures.as_completed(futures), total=len(futures),desc="Generate results"):
            pass
    
    write_thread.join()

    if output_place==f"{eval_dir}/{model}/{dataset}_qa_{lang}_2.json":
        os.remove(save_path)
        os.rename(new_output_path, save_path)