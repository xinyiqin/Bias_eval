source global.sh

MODEL=sensechat  #minimax/glm-4/sensechat/ernie/gpt-3.5
DATASET=stereoset #stereoset/bbq/crowspairs
LANG=en #en/zh

python evaluate.py \
    --data-path ./data \
    --output-path ./expr \
    --prompt-path ./expr/prompt \
    --eval-path ./eval \
    --word accurate \
    --model $MODEL \
    --dataset $DATASET \
    --lang $LANG \
    # --limit 5

python evaluate_all.py \
    --eval-path ./eval \
    --model $MODEL \
    --dataset $DATASET \
    --lang $LANG \

