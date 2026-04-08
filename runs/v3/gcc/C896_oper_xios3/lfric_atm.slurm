#!/bin/bash
#SBATCH --nodes=21
#SBATCH --exclusive
#SBATCH --time=00:30:00
#SBATCH --ntasks-per-node=288
#SBATCH --partition=standard
#SBATCH --qos=lowpriority
#SBATCH --distribution=block:block
#SBATCH --cpus-per-task=1
#SBATCH --hint=nomultithread    
#SBATCH --export=all

PROFILER="" # Choose between "heaptrack" , "hpctoolkit" for profiling and "" for no profiling.
export TRACE_MODEL_SINGLE_CORE=false # Only trace/profile the model on a single core of the model.
DEPENDENCIES_MODULES_PATH=/mnt/lustre/e1000/home/d435/d435/lparisid435/met-lfric-cirrus/environments/lfric/modules/Core # Path to load lfric dependencies modules. These will need to be generated first by spack

module load PrgEnv-gnu
module load cray-python
module use $DEPENDENCIES_MODULES_PATH
module load lfric-meta-gcc-xios3/3.1.1

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
export SRUN_CPUS_PER_TASK=1
export OMP_PLACES=cores
export LFRIC_ATM_EXEC=/work/d435/d435/lparisid435/met-lfric-cirrus/build_lfric/v3/lfric_apps_fast-debug_3.1.1_xios3/applications/lfric_atm/bin/lfric_atm

unset SLURM_NTASKS
unset SLURM_TASKS_PER_NODE
unset unset SLURM_TASKS_PER_NODE
unset SLURM_NPROCS
module load xthi


ulimit -c 0 # Do not create core dumps

export OMP_NUM_THREADS=4

srun --mem=0 --nodes=17 --cpus-per-task=4 --ntasks=1176   --hint=nomultithread  --distribution=block:block ./lfric_wrapper.sh  : --mem=0 --nodes=4 --ntasks=48 --cpus-per-task=4 --ntasks-per-node=12 --distribution=block:block --hint=nomultithread $LAUNCHER xios_server.exe