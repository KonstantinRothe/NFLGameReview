MODEL_PATH=experiments/baseline/best-valid_mt_bleu.pth
INPUT_TABLE=rotowire/valid.gtable
OUTPUT_SUMMARY=rotowire/valid.gtable_out

python model/summarize.py --model_path $MODEL_PATH --table_path $INPUT_TABLE --output_path $OUTPUT_SUMMARY --beam_size 4
