source global.sh
# belle-7b-2m/chinese-alpaca-2-7b/qwen-7b/openbuddy-70b/chatglm3-6b/llama2-chinese/baichuan2-13b/internlm2-1-8b/internlm2-20b/
MODEL=minimax #qwen-turbo/minimax/glm-4/sensechat/ernie/gpt-3.5-turbo-1106/gpt-3.5-turbo-0125/gpt-4-turbo
DATASET=crowspairs #stereoset/bbq/crowspairs
# LANG=en #en/zh

# for model in belle-7b-2m chinese-alpaca-2-7b qwen-7b openbuddy-70b chatglm3-6b llama2-chinese baichuan2-13b internlm2-1-8b internlm2-20b minimax glm-4 sensechat ernie gpt-3.5-turbo-1106 gpt-3.5-turbo-0125 gpt-4-turbo gemini
for model in minimax
do
    for dataset in cbbq stereoset bbq crowspairs
    do
        for lang in en zh
        do
            python evaluate/evaluate.py \
                --data-path ./data \
                --output-path ./expr \
                --prompt-path ./expr/prompt \
                --eval-path ./eval \
                --model $model \
                --dataset $dataset \
                --lang $lang \
                # --limit 5
        done
    done
done

