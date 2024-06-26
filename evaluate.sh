source global.sh

# Available models: belle-7b-2m chinese-alpaca-2-7b qwen-7b openbuddy-70b chatglm3-6b llama2-chinese baichuan2-13b internlm2-1-8b internlm2-20b abab-5.5 glm-4 sensechat ernie-3.5 gpt-3.5-turbo-1106 gpt-3.5-turbo-0125 gpt-4-turbo gemini
# Available datasets: cbbq stereoset bbq crowspairs
# Available languages: en zh

# MODEL="abab-5.5"
# DATASET="crowspairs"
# LANG="en"

MODEL=$1
DATASET=$2
LANG=$3

for model in $MODEL
do
    for dataset in $DATASET #cbbq stereoset bbq crowspairs
    do
        for lang in $LANG
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

