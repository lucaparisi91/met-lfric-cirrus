#!/bin/bash
#SBATCH --nodes=2
#SBATCH --exclusive
#SBATCH --time=00:20:00
#SBATCH --ntasks-per-node=24
#SBATCH --partition=standard
#SBATCH --qos=short
#SBATCH --distribution=block:block
#SBATCH --cpus-per-task=1
#SBATCH --hint=nomultithread    
#SBATCH --export=all

module load PrgEnv-gnu
module load cray-hdf5-parallel/1.14.3.5
module load cray-netcdf-hdf5parallel/4.9.0.17
module load spack
spack env activate /work/d435/d435/lparisid435/met-lfric-cirrus/environments/lfric
module load cray-python
spack load lfric-meta@3.0 %gcc
spack load pfunit

export FI_CXI_RX_MATCH_MODE=hybrid
#export FI_CXI_OPTIMIZED_MRS=false
export FI_CXI_DEFAULT_CQ_SIZE=1048576
export SRUN_CPUS_PER_TASK=8
export OMP_NUM_THREADS=$SRUN_CPUS_PER_TASK
export OMP_PLACES=cores

export LFRIC_ATM_EXEC=/work/d435/d435/shared/lparisid435/met-lfric-cirrus/build_lfric/v3/lfric_apps_3.1.1//applications/lfric_atm/bin/lfric_atm

unset SLURM_NTASKS
unset SLURM_TASKS_PER_NODE
unset unset SLURM_TASKS_PER_NODE
unset SLURM_NPROCS
module load xthi

ulimit -c 0 # Do not create core dumps

srun --nodes=1 --cpus-per-task=1 --ntasks=24  --hint=nomultithread  --distribution=block:block ./lfric_wrapper.sh  : --nodes=1 --ntasks=4 --cpus-per-task=4 --ntasks-per-node=4 --distribution=block:block --hint=nomultithread xios_server.exe