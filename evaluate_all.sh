
source global.sh

DATASET="stereoset bbq crowspairs cbbq cbbq_qa" #stereoset/bbq/crowspairs
LANG="en zh" #en/zh

python evaluate/evaluate_all.py \
    --eval-path ./eval \
    --dataset "$DATASET" \
    --lang "$LANG" \