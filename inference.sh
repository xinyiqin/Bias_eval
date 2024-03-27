source global.sh

MODEL=minimax #minimax/glm-4/sensechat/ernie/gpt-3.5/qwen-turbo/internlm2
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
    # --limit 5
