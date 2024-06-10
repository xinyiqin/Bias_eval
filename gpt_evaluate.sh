source global.sh

# belle-7b-2m/internlm2-20b/internlm2-1-8b/qwen-7b/openbuddy-70b/chatglm3-6b/baichuan2-13b/chinese-alpaca-2-7b/llama2-chinese
MODEL=ernie #gemini/minimax/glm-4/sensechat/ernie/gpt-4o/gpt-4-turbo/gpt-3.5-turbo-1106/gpt-3.5-turbo-0125/qwen-turbo/
EVALUATOR=gpt-4o-2024-05-13
DATASET=cbbq
# LANG=zh #en/zh
NUM_WORKERS=6

for model in gpt-4o
do
    for lang in en zh
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