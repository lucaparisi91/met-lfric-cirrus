#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=24:0:0
#SBATCH --partition=highmem
#SBATCH --qos=standard
#SBATCH --account=z04
#SBATCH --exclusive
#SBATCH --cpus-per-task=288

module load PrgEnv-gnu
module load cray-hdf5-parallel/1.14.3.5
module load cray-netcdf-hdf5parallel/4.9.0.17

EXE=/work/z04/shared/lparisi/software-cirrus-ex/spack-cirrus-ex/test_lfric/build_lfric/latest/lfric_core/mesh_tools/bin/cubedsphere_mesh_generator
export OMP_NUM_THREADS=288

srun --cpus-per-task=288 --hint=nomultithread $EXE NML_FILE_HERE

sacct -j $SLURM_JOB_ID --format=Elapsed
