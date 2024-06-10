
source global.sh

DATASET="crowspairs stereoset bbq cbbq cbbq_qa" #stereoset/bbq/crowspairs
LANG="en zh" #en/zh

python evaluate/evaluate_all.py \
    --eval-path ./eval \
    --dataset "$DATASET" \
    --lang "$LANG" \