. env.sh
cd lfric_apps/rose-stem
export CYLC_VERSION=8
cylc vip  -z group='gungho_model_gnu_fast' -s SITE="'cirrus'" -s ROSE_ORIG_HOST="'localhost'" -s CYLC_WORKFLOW_SRC_DIR="'$(pwd)'" -s HOUSEKEEPING=False -s HPC_ACCOUNT="'z19'" -s HPC_USERNAME="'lparisi'" -s OVERRIDE_LOG_LEVEL="''" -v .