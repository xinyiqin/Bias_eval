source global.sh
# openbuddy-70b/chatglm3-6b/llama2-chinese/baichuan2-13b/internlm2-1-8b/internlm2-20b/
MODEL=sensechat  #qwen-turbo/minimax/glm-4/sensechat/ernie/gpt-3.5-turbo-1106/gpt-3.5-turbo-0125/gpt-4-turbo
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

