#!/bin/bash
# Generate mesh partitions using cubed-sphere mesh generator
# First argument: Size of mesh (bit that goes after C in the file names)
# Second argument: Number of MPI ranks = Number of nodes*128/threads_per_rank
# Third argument: Start Partition 
# Fourth argument: Chunk size

set -x
set -e

CELLS_PER_DIM=$1
NRANKS=$2
START_PARTTION=$3
CHUNKSIZE=$4

SOURCE_DIR=/work/z04/shared/lparisi/software-cirrus-ex/spack-cirrus-ex/test_lfric/cylc/test_workflow/generate_mesh

mesh=C${CELLS_PER_DIM}

partition_start=$START_PARTTION

# Pick the partition range for this chunk
if [ $(( $NRANKS - partition )) -lt $CHUNKSIZE ]
then
    partition_end=$(( $NRANKS - 1 ))
else
    partition_end=$(( partition + CHUNKSIZE - 1 ))
fi

# Prepare the namelist
nmlname=${mesh}_${partition_start}-${partition_end}.nml

cp $SOURCE_DIR/cubedsphere_mesh_gen_blank.nml $nmlname

sed -i "s/  mesh_file_prefix  = /  mesh_file_prefix  = 'C$CELLS_PER_DIM'/" $nmlname
sed -i "s/  n_partitions        = /  n_partitions        = $NRANKS/" $nmlname

sed -i "s/  partition_range     = /  partition_range     = $partition_start, $partition_end/" $nmlname