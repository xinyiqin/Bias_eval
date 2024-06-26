source global.sh

# Available models: belle-7b-2m chinese-alpaca-2-7b qwen-7b openbuddy-70b chatglm3-6b llama2-chinese baichuan2-13b internlm2-1-8b internlm2-20b abab-5.5 glm-4 sensechat ernie-3.5 gpt-3.5-turbo-1106 gpt-3.5-turbo-0125 gpt-4-turbo gemini
# Available evaluator: gpt-4o-2024-05-13
# Available datasets: cbbq
# Available languages: en zh

# MODEL="ernie-3.5"
# EVALUATOR=gpt-4o-2024-05-13
# LANG="en zh"
# DATASET=cbbq
# NUM_WORKERS=6

MODEL=$1 
EVALUATOR=$2
LANG=$3
DATASET=$4
NUM_WORKERS=$5

for model in $MODEL
do
    for lang in $LANG
    do
        python gpt_evaluator/gpt_evaluate.py \
            --output-path ./eval \
            --expr-path ./expr \
            --evaluator_model $EVALUATOR \
            --eval_num 3 \
            --candidate_model $model \
            --dataset $DATASET \
            --lang $lang \
            --num_workers $NUM_WORKERS \
            # --limit 1
        python gpt_evaluator/sum_result.py \
            --output-path ./eval \
            --expr-path ./expr \
            --evaluator_model $EVALUATOR \
            --eval_num 3 \
            --candidate_model $model \
            --dataset $DATASET \
            --lang $lang \
            --num_workers $NUM_WORKERS \
            # --limit 1
    done
done