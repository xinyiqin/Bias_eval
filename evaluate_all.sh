
source global.sh

DATASET="crowspairs stereoset bbq cbbq" #stereoset/bbq/crowspairs
LANG="en zh" #en/zh

python evaluate_all.py \
    --eval-path ./eval \
    --dataset "$DATASET" \
    --lang "$LANG" \