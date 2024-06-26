source global.sh

# Available models:
# belle-7b-2m/internlm2-20b/internlm2-1-8b/qwen-7b/openbuddy-70b/chatglm3-6b/baichuan2-13b/chinese-alpaca-2-7b/llama2-chinese
# gemini/abab-5.5/glm-4/sensechat/ernie/gpt-4o/gpt-4-turbo/gpt-3.5-turbo-1106/gpt-3.5-turbo-0125/qwen-turbo/

# Available datasets: stereoset/bbq/crowspairs/cbbq
# Available languages: en/zh

# MODEL=gpt-4o 
# NUM_WORKERS=32
# DATASET="crowspairs"
# LANG="en"

MODEL=$1 
DATASET=$2 #stereoset/bbq/crowspairs/cbbq
LANG=$3 # en/zh
NUM_WORKERS=$4

for dataset in $DATASET
do
    for lang in $LANG
    do
        python inference/inference.py \
            --data-path ./data \
            --output-path ./expr \
            --prompt-path ./expr/prompt \
            --model $MODEL \
            --dataset $dataset \
            --lang $lang \
            --num_workers $NUM_WORKERS \
            --max_new_tokens 100 \
            --retry_times 5 \
            --answer_num 5 \
            # --limit 100 \
    done
done