source global.sh

# llama2-chinese/llama-13b/llama2-70b/llama-7b/internlm2/
MODEL=gemini #gemini/minimax/glm-4/sensechat/ernie/gpt-3.5-turbo-1106/gpt-3.5-turbo-0125/qwen-turbo/
DATASET=bbq #stereoset/bbq/crowspairs
LANG=en #en/zh
NUM_WORKERS=1

python inference.py \
    --data-path ./data \
    --output-path ./expr \
    --prompt-path ./expr/prompt \
    --word accurate \
    --model $MODEL \
    --dataset $DATASET \
    --lang $LANG \
    --num_workers $NUM_WORKERS \
    --max_new_tokens 100 \
    --retry_times 2 \
    # --limit 10 \