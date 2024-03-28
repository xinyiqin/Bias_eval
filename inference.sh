source global.sh

MODEL=gpt-4-turbo #minimax/glm-4/sensechat/ernie/gpt-3.5-turbo-1106/gpt-3.5-turbo-0125/qwen-turbo/internlm2/llama-13b
DATASET=stereoset #stereoset/bbq/crowspairs
LANG=en #en/zh
NUM_WORKERS=32

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
    # --limit 10
