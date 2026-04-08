# Cylc workflows

Automate running multiple benchmarks using cylc

## Setup cylc on first installation

```bash
module load cray-python
python3 -v venv /work/d435/d435/shared/lparisid435/benchmarks/cylc_env
source /work/d435/d435/shared/lparisid435/benchmarks/cylc_env/bin/activate
pip install -r requirements.txt
```

## Run the workflows

```bash
source env.sh
cylc vip
```