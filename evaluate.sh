source global.sh
# chinese-alpaca-2-7b/qwen-7b/openbuddy-70b/chatglm3-6b/llama2-chinese/baichuan2-13b/internlm2-1-8b/internlm2-20b/
MODEL=chinese-alpaca-2-7b #qwen-turbo/minimax/glm-4/sensechat/ernie/gpt-3.5-turbo-1106/gpt-3.5-turbo-0125/gpt-4-turbo
DATASET=cbbq #stereoset/bbq/crowspairs
LANG=en #en/zh

# for model in chinese-alpaca-2-7b qwen-7b openbuddy-70b chatglm3-6b llama2-chinese baichuan2-13b internlm2-1-8b internlm2-20b minimax glm-4 sensechat ernie gpt-3.5-turbo-1106 gpt-3.5-turbo-0125 gpt-4-turbo gemini
for model in minimax
do
    python evaluate.py \
        --data-path ./data \
        --output-path ./expr \
        --prompt-path ./expr/prompt \
        --eval-path ./eval \
        --model $model \
        --dataset $DATASET \
        --lang $LANG \
        # --limit 5
done

