# BiasEval: A Comprehensive Bias Evaluation on Generative AI

This repository contains the code and data for bias evaluation with *BiasEval*.

💡 BiasEval leaderboard: [BiasEval Leaderboard](https://xinyiqin.github.io/Bias_eval/leaderboard/).

## How to Use this Code
For bias evaluation with RedditBias, please use Evaluation/measure_bias.py. The rest of the code you can find in this repository documents the data set creation and offers other useful functions.

## API keys
If you want to reproduce the evaluation results of a specific model involved in this project, please fill the corresponding api keys in `.global.sh` file.

## Dataset

The evaluation datasets are now stored in the `./data` folder. The possible answers are stored in the `./expr` folder. 



To generate leaderboard statistics, there are two steps:

## Inference

### Single-choice inference
1. Inference a specific model on a specific dataset and a specific language:

For example, inference gpt-4o on crowspairs dataset in English with 32 workers, you should run:
```bash
bash inference.sh gpt-4o crowspairs en 32
```

2. Inference a specific model on multiple datasets and multiple languages, run:
```bash
bash inference.sh gpt-4o "crowspairs stereoset bbq cbbq" "en zh" 32
```

### Open-Question inference
```bash
bash inference_qa.sh gpt-4o cbbq "en zh" 32
```

## Evaluation

### Single-choice evaluation

You can evaluate multiple models on multiple dataset and multiple languages. 

For example:
```bash
bash evaluate.sh "abab-5.5 qwen-7b" "crowspairs stereoset" "en zh"
```

The evaluation results will be stored in the `./eval` folder.

### Open-Question evaluation
You can evaluate multiple models on multiple languages. You can use any gpt model as the evaluator. 

For example, we use gpt-4o as the evaluator:
```bash
bash gpt_evaluate.sh "ernie-3.5" gpt-4o-2024-05-13 "en zh" cbbq 6
```
The evaluation results will be stored in the `./eval` folder.

## Ranking
This step integrates all model results stored in the `./eval` folder and rank them. Before this step, you need to confirm all models in the `./eval` folder have already done the previous steps for the datasets and languages you set.

```bash
bash evaluate_all.sh "stereoset bbq crowspairs cbbq cbbq_qa" "en zh"
```

The ranking excel will be stored in the `./eval/leaderboard` folder.


## Evaluation for your model
Add the model inference code to the `./inference/generator` file or `./inference/generator_open_source` file.