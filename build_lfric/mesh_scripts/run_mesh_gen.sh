#!/bin/bash

# First argument: Size of mesh (bit that goes after C in the file names)
# Second argument: Number of MPI ranks = Number of nodes*128/threads_per_rank
set -x

mkdir -p C$1_"$2"
cd C$1_"$2"

partition=0
chunksize=2000
while [ $partition -lt $2 ]
do
    if [ $(( $4 - partition )) -lt $chunksize ]
    then
        partition_range=C$1_"$partition"_$(( $2 - 1 ))
    else
        partition_range=C$1_"$partition"_$(( partition + chunksize - 1 ))
    fi
    nmlname=$partition_range.nml
    subname=mesh_gen_$partition_range.slurm

    cp ../cubedsphere_mesh_gen_blank.nml $nmlname
    cp ../mesh_gen_blank.slurm $subname

    sed -i "s/  mesh_file_prefix  = /  mesh_file_prefix  = 'C$1'/" $nmlname
    sed -i "s/  n_partitions        = /  n_partitions        = $2/" $nmlname
    if [ $(( $2 - partition )) -lt $chunksize ]
    then
        sed -i "s/  partition_range     = /  partition_range     = $partition, $(( $2 - 1 ))/" $nmlname
    else
        sed -i "s/  partition_range     = /  partition_range     = $partition, $(( partition + chunksize - 1 ))/" $nmlname
    fi

    sed -i "s/NML_FILE_HERE/$nmlname/" $subname

    sbatch -J mesh_gen_$partition_range $subname

    partition=$(( partition + chunksize ))
done
