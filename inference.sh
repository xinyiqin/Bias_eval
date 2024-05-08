source global.sh

# internlm2-20b/internlm2-1-8b/qwen-7b/openbuddy-70b/chatglm3-6b/baichuan2-13b/chinese-alpaca-2-7b/llama2-chinese
MODEL=gemini #gemini/minimax/glm-4/sensechat/ernie/gpt-4-turbo/gpt-3.5-turbo-1106/gpt-3.5-turbo-0125/qwen-turbo/
DATASET=bbq #stereoset/bbq/crowspairs
LANG=zh #en/zh
NUM_WORKERS=3

python inference.py \
    --data-path ./data \
    --output-path ./expr \
    --prompt-path ./expr/prompt \
    --model $MODEL \
    --dataset $DATASET \
    --lang $LANG \
    --num_workers $NUM_WORKERS \
    --max_new_tokens 100 \
    --retry_times 2 \
    # --limit 100 \