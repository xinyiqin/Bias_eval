source global.sh

# internlm2-20b/internlm2-1-8b/qwen-7b/openbuddy-70b/chatglm3-6b/baichuan2-13b/chinese-alpaca-2-7b/llama2-chinese
MODEL=sensechat #gemini/minimax/glm-4/sensechat/ernie/gpt-4-turbo/gpt-3.5-turbo-1106/gpt-3.5-turbo-0125/qwen-turbo/
DATASET=cbbq #stereoset/bbq/crowspairs
# LANG=zh #en/zh
NUM_WORKERS=1

for lang in en
do
    python inference.py \
        --data-path ./data \
        --output-path ./expr \
        --prompt-path ./expr/prompt \
        --model $MODEL \
        --dataset $DATASET \
        --lang $lang \
        --num_workers $NUM_WORKERS \
        --max_new_tokens 100 \
        --retry_times 2 \
        --answer_num 5 \
        # --limit 100 \
done