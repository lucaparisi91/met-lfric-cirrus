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

SOURCE_DIR=${CYLC_RUN_DIR}/${CYLC_WORKFLOW_ID}/generate_mesh

mesh=C${CELLS_PER_DIM}
partition_start=$START_PARTTION

# Pick the partition range for this chunk
if [ $((  partition_start + CHUNKSIZE )) -gt $NRANKS ]
then
    partition_end=$(( $NRANKS - 1 ))
else
    echo "b"
    partition_end=$(( partition_start + CHUNKSIZE - 1 ))
fi

# Prepare the namelist
nmlname=${mesh}.nml

cp $SOURCE_DIR/cubedsphere_mesh_gen_blank.nml $nmlname

sed -i "s/  mesh_file_prefix  = /  mesh_file_prefix  = 'C$CELLS_PER_DIM'/" $nmlname
sed -i "s/  n_partitions        = /  n_partitions        = $NRANKS/" $nmlname

sed -i "s/  partition_range     = /  partition_range     = $partition_start, $partition_end/" $nmlname