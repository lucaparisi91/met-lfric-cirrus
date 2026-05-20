#!/bin/bash
#SBATCH --nodes=6
#SBATCH --exclusive
#SBATCH --time=00:70:00
#SBATCH --ntasks-per-node=288
#SBATCH --partition=standard
#SBATCH --reservation=determinism_testing
#SBATCH --qos=reservation
#SBATCH --distribution=block:block
#SBATCH --cpus-per-task=1
#SBATCH --hint=nomultithread    
#SBATCH --exclusive

set -e

PROFILER="" # Choose between "heaptrack" , "hpctoolkit" for profiling and "" for no profiling.
DEPENDENCIES_MODULES_PATH=/work/z19/shared/lparisi/met-lfric-cirrus/environments/lfric/modules/Core # Path to load lfric dependencies modules. These will need to be generated first by spack
XIOS="xios2" # XIOS version to run with. Allowed values are xios2 and xios3
CRAYPAT=1 # Whether to instrument the executable with Craypat

module load PrgEnv-gnu
module load cray-python
module use $DEPENDENCIES_MODULES_PATH
module --ignore_cache load "lfric-meta-gcc-xios2/3.1.1"

# Wrap executable with heaptrack, if doing memory tracking
if [ "$PROFILER" = "heaptrack" ]; then
    export LAUNCHER="heaptrack"
    module load heaptrack-gcc
else
    if [ "$PROFILER" = "hpctoolkit" ]; then
        export LAUNCHER="hpcrun"
        module load hpctoolkit-gcc
    else 
        export LAUNCHER=""
    fi
fi

export FI_CXI_RX_MATCH_MODE=hybrid
#export FI_CXI_OPTIMIZED_MRS=false
export FI_CXI_DEFAULT_CQ_SIZE=1048576

export EXE=/work/z19/shared/lparisi/met-lfric-cirrus/build_lfric/v3/lfric_apps_production_3.1.1_${XIOS}/applications/gungho_model/bin/gungho_model

if [ $CRAYPAT -eq 1 ]; then
    EXE=/work/z19/shared/lparisi/met-lfric-cirrus/build_lfric/v3/lfric_apps_production_3.1.1_${XIOS}_craypat/applications/gungho_model/bin/gungho_model+pat+mpi
fi

unset SLURM_NTASKS
unset SLURM_TASKS_PER_NODE
unset unset SLURM_TASKS_PER_NODE
unset SLURM_NPROCS
module load xthi

ulimit -c 0 # Do not create core dumps
EXPERIMENTS_FOLDER=$(pwd)/performance_determinism

if [ "$CRAYPAT" -eq 1 ]; then
   EXPERIMENTS_FOLDER="${EXPERIMENTS_FOLDER}_craypat"
fi

TEMPLATES_FOLDER=$(pwd)/template
N=1 # Number of runs to perform
BASE_JOB_NAME="$EXPERIMENTS_FOLDER/gungho_model_run_$(date +%Y%m%d_%H%M%S)_$SLURM_NODELIST"


for i in $(seq 1 10); do
    for thread in 1 2 4; do
        JOB_FOLDER="${BASE_JOB_NAME}_t$thread_$i"
        mkdir -p $JOB_FOLDER
        cd $JOB_FOLDER
        cp $TEMPLATES_FOLDER/* .
        NTASKS=$((1728 / thread))
        
        export SRUN_CPUS_PER_TASK=$thread
        export OMP_PLACES=cores
        export OMP_NUM_THREADS=$thread

        srun --mem=0 --ntasks=$NTASKS --cpus-per-task=$thread --hint=nomultithread  --distribution=block:block $EXE configuration.nml
        
    done
done