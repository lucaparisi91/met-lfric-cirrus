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

You will need to copy here the templates directory, containing inputfiles and meshes.
These are too bigs to fit on a repo.

```bash
source env.sh
cylc vip
```

## Analyse the data

Use the `collect` python module to collect data from a volder. For example to collect vernier timings use

```bash
source env.sh
python -m collect --vernier /work/d435/d435/shared/lparisid435/benchmarks/runs/cylc-run/workflows/runN/share
```

to collect cylc outputs in the `/work/d435/d435/shared/lparisid435/benchmarks/runs/cylc-run/workflows/runN/share` folder.
