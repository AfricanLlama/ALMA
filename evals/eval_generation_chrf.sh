OUTPUT_DIR=${1}
TEST_PAIRS=${2}

## Evaluation
source ~/miniconda3/bin/activate
conda activate alma-eval
for pair in ${TEST_PAIRS//,/ }; do
    src=$(echo ${pair} | cut -d "-" -f 1)
    tgt=$(echo ${pair} | cut -d "-" -f 2)
    TOK="13a"
    other="en"
    if [ ${src} == "en" ]; then
        other=${tgt}
    else 
        other=${src}
    fi
    echo "--------------------Results for ${pair}-------------------------------------"
    # Data path is the path to the test set.
    data_path=./data/${other}en/test.${other}-en.${tgt}
    output_path=${OUTPUT_DIR}/test-${src}-${tgt}
    SACREBLEU_FORMAT=text sacrebleu -tok ${TOK} -w 2 ${output_path} < ${data_path} > ${output_path}.bleu
    cat ${output_path}.bleu
    CHRF_FORMAT=text sacrebleu -m chrf --chrf-word-order 2 ${output_path} < ${data_path} > ${output_path}.chrf
    cat ${output_path}.chrf
done

for pair in ${TEST_PAIRS//,/ }; do
    src=$(echo ${pair} | cut -d "-" -f 1)
    tgt=$(echo ${pair} | cut -d "-" -f 2)
    echo "---------------------------${src}-${tgt}-------------------------------"
    output_path=${OUTPUT_DIR}/test-${src}-${tgt}
    cat ${output_path}.chrf
done
