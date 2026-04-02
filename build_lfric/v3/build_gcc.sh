
OPT=fast-debug # Optimisiation level to pass to ghungho_model: debug, fast-debug, production
CRAYPAT=0 # Wether to instrument the execuatable with Craypat
DOWNLOAD=0 # Whether to download the model code from code.metoffice.gov.uk
RELEASE_APPS=3.1.1 # LFRic release to checkout from github
RELEASE_CORE=3.1 # LFRic release to checkout from github  
CLEAN=0 # Whether to clean the build directory before building
MODEL=lfric_atm # App to build, i.e. lfric_atm or ghungho_model
DEPENDENCIES_MODULES_PATH=/work/d435/d435/shared/lparisid435/met-lfric-cirrus/environments/lfric/modules/Core # Path to load lfric dependencies modules. These will need to be generated first by spack
set -e  # Stop the script if any command fails

module use $DEPENDENCIES_MODULES_PATH # Make modules with lfric dependencies available. 
module load lfric-meta-gcc/3.1.1
module load PrgEnv-gnu
module load cray-hdf5-parallel/1.14.3.5
module load cray-netcdf-hdf5parallel/4.9.0.17
module load cray-python

# Enable perftools if CRAYPAT is set
if [ $CRAYPAT -eq 1 ]; then
    module load perftools-base
    module load perftools
fi

set -x

ROOT_DIR=$(pwd)

LFRIC_APPS_DIR=lfric_apps_$OPT_$RELEASE_APPS
LFRIC_CORE_DIR=lfric_core_$OPT_$RELEASE_CORE


# Add _craypat to directory names if CrayPat is enabled
if [ $CRAYPAT -eq 1 ]; then
    LFRIC_APPS_DIR=${LFRIC_APPS_DIR}_craypat
    LFRIC_CORE_DIR=${LFRIC_CORE_DIR}_craypat
fi

# --- Download the model code if enabled ---
if [ $DOWNLOAD -eq 1 ]; then
    rm -irf $LFRIC_APPS_DIR $LFRIC_CORE_DIR
    git clone -b vn$RELEASE_APPS git@github.com:MetOffice/lfric_apps.git $LFRIC_APPS_DIR
    
    git clone -b vn$RELEASE_CORE git@github.com:MetOffice/lfric_core.git $LFRIC_CORE_DIR
    
fi

# export FFLAGS="-I $XIOS_ROOT/inc -I /software/projects/pawsey0835/ddeeptimahanti/setonix/2025.08/software/linux-sles15-zen3/gcc-14.2.0/yaxt-0.11.3-vxxancnxeqjvwc5nx7zm4kyw6b3f56bu/include/"
# export LIBRARY_PATH=$XIOS_ROOT/lib:$LIBRARY_PATH
# export LDFLAGS="-L $XIOS_ROOT/lib -I $XIOS_ROOT/inc -Wl,-rpath=$XIOS_ROOT/lib "

cd $LFRIC_APPS_DIR/build
export CRAY_ENVIRONMENT=TRUE
export PE_ENV=GNU
export FC=ftn
# PFUNIT_ROOT=/mnt/lustre/e1000/home/z04/shared/lparisi/software-cirrus-ex/spack-cirrus-ex/test_lfric/lfric/opt/linux-rhel9-zen5/gcc-14.2/pfunit-4.12.0-vdluwg5aqey56trb6u5t7fumvwqymbps/PFUNIT-4.12 
# export PATH=$PFUNIT_ROOT/bin:$PATH
# export FFLAGS="-I $PFUNIT_ROOT/include $FFLAGS"
# export LIBRARYPATH=$PFUNIT_ROOT/lib:$LIBRARYPATH

if [ $CLEAN -eq 1 ]; then
    rm -rf $ROOT_DIR/$LFRIC_APPS_DIR/applications/$MODEL/working/
fi


VERBOSE=3 python local_build.py -p "meto-azspice" -v  -c ../../$LFRIC_CORE_DIR -o $OPT $MODEL -j 16 2>&1 | tee $ROOT_DIR/build_gcc.log

# If craypat is enabled, instrument the model

if [ $CRAYPAT -eq 1 ]; then
    cd $ROOT_DIR/$LFRIC_APPS_DIR/applications/$MODEL/bin
    rm -f ${MODEL}+pat*
    pat_build $MODEL -o ${MODEL}+pat+sampling
    pat_build -g mpi $MODEL -o ${MODEL}+pat+mpi
    pat_build -g omp $MODEL -o ${MODEL}+pat+omp
    
    
fi