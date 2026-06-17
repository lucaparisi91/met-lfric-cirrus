set -e # Stop the script if any command fails
set -x # Print each command before executing it for easier debugging

OPT=fast-debug # Optimisiation level to pass to ghungho_model: full-debug, fast-debug, production
CRAYPAT=0 # Wether to instrument the execuatable with Craypat
DOWNLOAD=0 # Whether to download the model code from code.metoffice.gov.uk
RELEASE_CORE=3.1 # LFRic release to checkout from github  
CLEAN=0 # Whether to clean the build directory before building
XIOS="xios3" # XIOS version to build with. Allowed values are xios2 and xios3 
DEPENDENCIES_MODULES_PATH=/mnt/lustre/e1000/home/d435/d435/lparisid435/met-lfric-cirrus/environments/lfric/modules/Core # Path to load lfric dependencies modules. These will need to be generated first by spack
MODEL=io_demo
export RDEF_PRECISION="32" # ? 
export R_TRAN_PRECISION="32"  # Transport scheme precision ?
export R_BL_PRECISION="32" # Boundary layer scheme precision ?
export R_SOLVER_PRECISION="32" # Precision of the solver
export R_PHYS_PRECISION="32" # Precision of physics scheme

set +x  # Disable command echoing to limit noise from module loading


module use $DEPENDENCIES_MODULES_PATH # Make modules with lfric dependencies available. 
module -I load lfric-meta-gcc-no-xios/3.1.1
module load PrgEnv-gnu
module load cray-hdf5-parallel/1.14.3.5
module load cray-netcdf-hdf5parallel/4.9.0.17
module load cray-python

# # Enable perftools if CRAYPAT is set
# if [ $CRAYPAT -eq 1 ]; then
#     module load perftools-base
#     module load perftools
# fi

set -x # Re-enable command echoing after loading modules

ROOT_DIR=$(pwd)

LFRIC_CORE_DIR=lfric_core_${OPT}_${RELEASE_CORE}_${XIOS}


# --- Download the model code if enabled ---
if [ $DOWNLOAD -eq 1 ]; then
    rm -irf  $LFRIC_CORE_DIR
    
    git clone -b vn$RELEASE_CORE git@github.com:MetOffice/lfric_core.git $LFRIC_CORE_DIR
    
fi

XIOS_ROOT="/work/d435/d435/lparisid435/met-lfric-cirrus/build_lfric/xios/$XIOS"
export FFLAGS="-I $XIOS_ROOT/inc $FFLAGS"
export LIBRARY_PATH=$XIOS_ROOT/lib:$LIBRARY_PATH
export LDFLAGS="-L $XIOS_ROOT/lib -I $XIOS_ROOT/inc -Wl,-rpath=$XIOS_ROOT/lib $LDFLAGS"

export CRAY_ENVIRONMENT=TRUE
export PE_ENV=GNU
export FC=ftn
# PFUNIT_ROOT=/mnt/lustre/e1000/home/z04/shared/lparisi/software-cirrus-ex/spack-cirrus-ex/test_lfric/lfric/opt/linux-rhel9-zen5/gcc-14.2/pfunit-4.12.0-vdluwg5aqey56trb6u5t7fumvwqymbps/PFUNIT-4.12 
# export PATH=$PFUNIT_ROOT/bin:$PATH
# export FFLAGS="-I $PFUNIT_ROOT/include $FFLAGS"
# export LIBRARYPATH=$PFUNIT_ROOT/lib:$LIBRARYPATH

if [ $CLEAN -eq 1 ]; then
    rm -rf $ROOT_DIR/$LFRIC_CORE_DIR/applications/$MODEL/working/
fi

export LDMPI=ftn
export FPP="cpp -P -traditional"

cd $LFRIC_CORE_DIR/applications/io_demo

export LIBRARY_PATH=$PFUNIT/lib:$LIBRARY_PATH

make -j 8
# If craypat is enabled, instrument the model

# if [ $CRAYPAT -eq 1 ]; then
#     cd $ROOT_DIR/$LFRIC_APPS_DIR/applications/$MODEL/bin
#     rm -f ${MODEL}+pat*
#     pat_build $MODEL -o ${MODEL}+pat+sampling
#     pat_build -g mpi $MODEL -o ${MODEL}+pat+mpi
#     pat_build -g omp $MODEL -o ${MODEL}+pat+omp
    
# fi