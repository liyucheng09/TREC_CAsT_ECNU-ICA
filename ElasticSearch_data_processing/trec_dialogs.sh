export BERT_BASE_DIR=bert/bert-base-uncased
export GLUE_DIR=bert/glue_data
export TRAINED_CLASSIFIER=bert/mrpc_output
export INPUT_DIR=bert/test
export OUTPUT_DIR=bert/test
export QUERY_DIR=queries.txt
export KEYWORD_MOD=rake
export CANDIDATE_NUMBER=10000

python pipeline.py $QUERY_DIR $KEYWORD_MOD $CANDIDATE_NUMBER
python bert/run_classifier.py \
  --task_name=MRPC \
  --do_predict=true \
  --data_dir=$INPUT_DIR \
  --vocab_file=$BERT_BASE_DIR/vocab.txt \
  --bert_config_file=$BERT_BASE_DIR/bert_config.json \
  --init_checkpoint=$TRAINED_CLASSIFIER \
  --max_seq_length=128 \
  --output_dir=$OUTPUT_DIR >/dev/null 2>&1
python get_answers.py $OUTPUT_DIR/test.tsv $OUTPUT_DIR/test_results.tsv
