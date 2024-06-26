
source global.sh

# DATASET="stereoset bbq crowspairs cbbq cbbq_qa"
# LANG="en zh"

DATASET=$1
LANG=$2

python evaluate/evaluate_all.py \
    --eval-path ./eval \
    --dataset "$DATASET" \
    --lang "$LANG" \