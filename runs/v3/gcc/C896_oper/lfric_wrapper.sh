#! /bin/bash


# On MPI rank 0 turn on core file creation
if [ "$SLURM_PROCID" -eq 0 ]; then
    ulimit -c unlimited

else
    ulimit -c 0
    if [ "$TRACE_MODEL_SINGLE_CORE" = true ]; then # Disable profiling or tracing on ranks other than 0.
        export LAUNCHER="" 
    fi
fi


$LAUNCHER ${LFRIC_ATM_EXEC} configuration.nml