# Using cylc

## Install the environments

Install the spack environment. From the root of this repository

```bash
module load spack
spack env activate environments/lfric
spack module lmode refresh --delete-tree -y
```

Install the cylc python environment. 
From the root of this folder

```bash
cd cirrus_lfric
python -m venv .venv
source .venv/bin/activate
pip install .
```


## Run an example

Clone the v3.2 branch with the cirrus site

```bash
git clone -b cirrus_site git@github.com:lucaparisi91/lfric_apps.git 
```

Run the group `gungho_model_gnu_fast` on the `z19` account using

```bash
cd lfric_apps/rose-stem
export CYLC_VERSION=8
cylc vip  -z group='gungho_model_gnu_fast' -s SITE="'cirrus'" -s ROSE_ORIG_HOST="'localhost'" -s CYLC_WORKFLOW_SRC_DIR="'$(pwd)'" -s HOUSEKEEPING=False -s HPC_ACCOUNT="'z19'" -s HPC_USERNAME="'lparisi'" -v .
```

The `HOUSEKEEPING` variable is set to false, to avoid temporary files being deleted at the end of the run.