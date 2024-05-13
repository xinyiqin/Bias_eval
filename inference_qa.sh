source global.sh

# internlm2-20b/internlm2-1-8b/qwen-7b/openbuddy-70b/chatglm3-6b/baichuan2-13b/chinese-alpaca-2-7b/llama2-chinese
MODEL=openbuddy-70b #gemini/minimax/glm-4/sensechat/ernie/gpt-4-turbo/gpt-3.5-turbo-1106/gpt-3.5-turbo-0125/qwen-turbo/
DATASET=cbbq #stereoset/bbq/crowspairs
LANG=zh #en/zh
NUM_WORKERS=32

for lang in zh en
do
    python inference_qa.py \
        --data-path ./data \
        --output-path ./expr \
        --prompt-path ./expr/prompt \
        --model $MODEL \
        --dataset $DATASET \
        --lang $lang \
        --num_workers $NUM_WORKERS \
        --max_new_tokens 512 \
        --retry_times 2 \
        --answer_num 1 \
        # --limit 10 \
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