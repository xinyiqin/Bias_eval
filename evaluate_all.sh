
source global.sh

DATASET="crowspairs stereoset bbq" #stereoset/bbq/crowspairs
LANG=en #en/zh

python evaluate_all.py \
    --eval-path ./eval \
    --dataset "$DATASET" \
    --lang $LANG \