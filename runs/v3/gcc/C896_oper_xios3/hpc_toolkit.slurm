#!/bin/bash
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=00:30:00
#SBATCH --ntasks-per-node=288
#SBATCH --partition=standard
#SBATCH --qos=lowpriority
#SBATCH --distribution=block:block
#SBATCH --cpus-per-task=1
#SBATCH --hint=nomultithread    
#SBATCH --export=all


PROFILER="hpctoolkit" # Choose between "heaptrack" and "hpctoolkit" for profiling.
export TRACE_MODEL_SINGLE_CORE=false # Only trace/profile the model on a single core of the model.

module load PrgEnv-gnu
module load cray-python
module use /work/d435/d435/shared/lparisid435/met-lfric-cirrus/environments/lfric/modules/Core
module load lfric-meta-gcc/3.1.0
module load hpctoolkit-gcc

date
hpcstruct hpctoolkit-lfric_atm-measurements-148290/
date
hpcprof hpctoolkit-lfric_atm-measurements-148290/
date