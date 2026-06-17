#!/bin/bash
#SBATCH --nodes=2
#SBATCH --exclusive
#SBATCH --time=00:20:00
#SBATCH --ntasks-per-node=288
#SBATCH --partition=standard
#SBATCH --qos=short
#SBATCH --distribution=block:block
#SBATCH --cpus-per-task=1
#SBATCH --hint=nomultithread    
#SBATCH --export=all

PROFILER="" # Choose between "heaptrack" , "hpctoolkit","craypat" for profiling and "" for no profiling.
export TRACE_MODEL_SINGLE_CORE=false # Only trace/profile the model on a single core of the model.
DEPENDENCIES_MODULES_PATH=/mnt/lustre/e1000/home/d435/d435/lparisid435/met-lfric-cirrus/environments/lfric/modules/Core # Path to load lfric dependencies modules. These will need to be generated first by spack
XIOS="xios3" # XIOS version to run with. Allowed values are xios2 and xios3

XIOS_ROOT="/work/d435/d435/lparisid435/met-lfric-cirrus/build_lfric/xios/$XIOS"

XIOS_EXEC=$XIOS_ROOT/bin/xios_server.exe
CRAYPAT=1


module load PrgEnv-gnu
module load cray-python
module use $DEPENDENCIES_MODULES_PATH
module -I load lfric-meta-gcc-no-xios/3.1.1

# Wrap executable with heaptrack, if doing memory tracking
if [ "$PROFILER" = "heaptrack" ]; then
    export LAUNCHER="heaptrack"
    module load heaptrack-gcc
else
    if [ "$PROFILER" = "hpctoolkit" ]; then
        export LAUNCHER="hpcrun -o hpctoolkit-lfric_atm-$XIOS"
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
export LFRIC_ATM_EXEC=/work/d435/d435/lparisid435/met-lfric-cirrus/build_lfric/v3/lfric_apps_fast-debug_3.1.1_${XIOS}/applications/lfric_atm/bin/lfric_atm

unset SLURM_NTASKS
unset SLURM_TASKS_PER_NODE
unset unset SLURM_TASKS_PER_NODE
unset SLURM_NPROCS
module load xthi


ulimit -c 0 # Do not create core dumps

if [ "$PROFILER" = "craypat" ]; then
    export XIOS_EXEC="${XIOS_EXEC}+pat+mpi"
    LFRIC_ATM_EXEC="${LFRIC_ATM_EXEC}+pat+mpi"

fi

srun --mem=0 --nodes=1 --cpus-per-task=1 --ntasks=24  --hint=nomultithread  --distribution=block:block ./lfric_wrapper.sh  : --mem=0 --nodes=1 --ntasks=4 --cpus-per-task=4 --ntasks-per-node=4 --distribution=block:block --hint=nomultithread $LAUNCHER $XIOS_EXEC