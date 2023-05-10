#!/usr/bin/env bash

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

export LEARNING_RATE_IN=${LEARNING_RATE_IN:-"0.25"}
export LEARNING_RATE_FINAL=${LEARNING_RATE_FINAL:-"0.0001"}
export EPOCHS_NUMBER=${EPOCHS_NUMBER:-"100"}
export SQ_BOND_DIM=${SQ_BOND_DIM:-"5"}
export SQ_BOND_DIM_TRAINING=${SQ_BOND_DIM_TRAINING:-"7"}
export TIME_STEPS=${TIME_STEPS:-"20"}
export SAMPLES_NUMBER=${SAMPLES_NUMBER:-"1000"}
export TOTAL_SAMPLES_NUMBER=${TOTAL_SAMPLES_NUMBER:-"100000"}
export LOCAL_CHOI_RANK=${LOCAL_CHOI_RANK:-"1"}
export LOCAL_CHOI_RANK_TRAINING=${LOCAL_CHOI_RANK_TRAINING:-"4"}
export SEED=${SEED:-"42"}

get_all_parameters() {
cat << EOF
LEARNING_RATE_IN=${LEARNING_RATE_IN}
LEARNING_RATE_FINAL=${LEARNING_RATE_FINAL}
EPOCHS_NUMBER=${EPOCHS_NUMBER}
SQ_BOND_DIM=${SQ_BOND_DIM}
SQ_BOND_DIM_TRAINING=${SQ_BOND_DIM_TRAINING}
TIME_STEPS=${TIME_STEPS}
SAMPLES_NUMBER=${SAMPLES_NUMBER}
TOTAL_SAMPLES_NUMBER=${TOTAL_SAMPLES_NUMBER}
LOCAL_CHOI_RANK=${LOCAL_CHOI_RANK}
LOCAL_CHOI_RANK_TRAINING=${LOCAL_CHOI_RANK_TRAINING}
SEED=${SEED}
EOF
}

get_help() {
cat << EOF
Usage
--test:                  runs tests;
--typecheck:             runs static code analysis;
--lint:                  runs linter;
--bench:                 runs benchmarks;
--gen_rand_im [-n name]: generates a random IM and saves it, optionally accepts name of the experiment (default to "random_im");
--gen_samples [-n name]: generates samples from saved IM, optionally accepts name of the experiment (default to "random_im");
--train_im    [-n name]: trains IM on saved samples, optionally accepts name of the experiment (default to "random_im");
--get_params:          prints all the environment variables essential for a numerical experiment;
--help                   drops this message.
EOF
}

case $1 in

  --test)
        python3.10 -m pytest
    ;;
  --typecheck)
        python3.10 -m mypy --exclude /qgoptax/ "${script_dir}/../src"
    ;;
  --lint)
        pylint --ignore-paths="${script_dir}/../src/qgoptax" "${script_dir}/../src"
    ;;
  --bench)
        "${script_dir}/../src/benchmarks.py"
    ;;
  --gen_rand_im)
        shift
        "${script_dir}/../src/random_im.py" "$@"
    ;;
  --gen_samples)
        shift
        "${script_dir}/../src/gen_samples.py" "$@"
    ;;
  --train_im)
        shift
        "${script_dir}/../src/train_im.py" "$@"
    ;;
  --get_params)
        get_all_parameters
    ;;
  --help)
        get_help
    ;;
  *)
        echo "Unknown option: '$1'"
        get_help
        exit 1
    ;;
  
esac
