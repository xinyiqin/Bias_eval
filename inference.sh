source global.sh

# belle-7b-2m/internlm2-20b/internlm2-1-8b/qwen-7b/openbuddy-70b/chatglm3-6b/baichuan2-13b/chinese-alpaca-2-7b/llama2-chinese
MODEL=glm-4 #gemini/minimax/glm-4/sensechat/ernie/gpt-4o/gpt-4-turbo/gpt-3.5-turbo-1106/gpt-3.5-turbo-0125/qwen-turbo/
DATASET=bbq #stereoset/bbq/crowspairs/cbbq
# LANG=zh #en/zh
NUM_WORKERS=20

for dataset in bbq
do
    for lang in zh
    do
        python inference/inference.py \
            --data-path ./data \
            --output-path ./expr \
            --prompt-path ./expr/prompt \
            --model $MODEL \
            --dataset $dataset \
            --lang $lang \
            --num_workers $NUM_WORKERS \
            --max_new_tokens 100 \
            --retry_times 2 \
            --answer_num 5 \
            # --limit 100 \
    done
done

# for dataset in cbbq
# do
#     for lang in en zh
#     do
#         python inference/inference_qa.py \
#             --data-path ./data \
#             --output-path ./expr \
#             --prompt-path ./expr/prompt \
#             --model $MODEL \
#             --dataset $dataset \
#             --lang $lang \
#             --num_workers $NUM_WORKERS \
#             --max_new_tokens 512 \
#             --retry_times 2 \
#             --answer_num 1 \
#             # --limit 10 \
#     done
# done