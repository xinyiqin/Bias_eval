source global.sh
# baichuan2-13b/internlm2-1-8b/internlm2-20b/llama-7b/llama-13b
MODEL=gpt-4-turbo  #qwen-turbo/minimax/glm-4/sensechat/ernie/gpt-3.5-turbo-1106/gpt-3.5-turbo-0125
DATASET=crowspairs #stereoset/bbq/crowspairs
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

