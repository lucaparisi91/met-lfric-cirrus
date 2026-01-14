
OPT=fast-debug # Optimisiation level to pass to ghungho_model: debug, fast-debug, production
CRAYPAT=1 # Wether to instrument the execuatable with Craypat
DOWNLOAD=0 # Whether to download the model code from code.metoffice.gov.uk


# Load environment modules and activate spack environment
source ../../env.sh
module load spack
spack env activate ../environments/lfric
module load cray-python
spack load lfric-meta@2.2
spack load pfunit
spack load subversion
module load PrgEnv-gnu

module load cray-hdf5-parallel/1.14.3.5
module load cray-netcdf-hdf5parallel/4.9.0.17

# Enable perftools if CRAYPAT is set
if [ $CRAYPAT -eq 1 ]; then
    module load perftools-base
    module load perftools
fi

ROOT_DIR=$(pwd)

LFRIC_APPS_DIR=lfric_apps_$OPT
LFRIC_CORE_DIR=lfric_core_$OPT

# Add _craypat to directory names if CrayPat is enabled
if [ $CRAYPAT -eq 1 ]; then
    LFRIC_APPS_DIR=${LFRIC_APPS_DIR}_craypat
    LFRIC_CORE_DIR=${LFRIC_CORE_DIR}_craypat
fi

# --- Download the model code if enabled ---
if [ $DOWNLOAD -eq 1 ]; then
    svn co -r 11231 http://code.metoffice.gov.uk/svn/lfric_apps/main/trunk $LFRIC_APPS_DIR
    svn co -r 53041 https://code.metoffice.gov.uk/svn/lfric/LFRic/trunk $LFRIC_CORE_DIR
fi


# export FFLAGS="-I $XIOS_ROOT/inc -I /software/projects/pawsey0835/ddeeptimahanti/setonix/2025.08/software/linux-sles15-zen3/gcc-14.2.0/yaxt-0.11.3-vxxancnxeqjvwc5nx7zm4kyw6b3f56bu/include/"
# export LIBRARY_PATH=$XIOS_ROOT/lib:$LIBRARY_PATH
# export LDFLAGS="-L $XIOS_ROOT/lib -I $XIOS_ROOT/inc -Wl,-rpath=$XIOS_ROOT/lib "

cd $LFRIC_APPS_DIR/build
export CRAY_ENVIRONMENT=TRUE
export PE_ENV=GNU
export FC=ftn
PFUNIT_ROOT=/mnt/lustre/e1000/home/z04/shared/lparisi/software-cirrus-ex/spack-cirrus-ex/test_lfric/lfric/opt/linux-rhel9-zen5/gcc-14.2/pfunit-4.12.0-vdluwg5aqey56trb6u5t7fumvwqymbps/PFUNIT-4.12 
export PATH=$PFUNIT_ROOT/bin:$PATH
export FFLAGS="-I $PFUNIT_ROOT/include $FFLAGS"
export LIBRARYPATH=$PFUNIT_ROOT/lib:$LIBRARYPATH

VERBOSE=1 python local_build.py -p "meto-azspice" -c ../../$LFRIC_CORE_DIR -o $OPT -a gungho_model -j 16 2>&1 | tee build_gcc.log

# If craypat is enabled, instrument ghungho model
cd ../applications/gungho_model/bin

if [ $CRAYPAT -eq 1 ]; then
    rm -f gungho_model+pat*
    pat_build gungho_model -o gungho_model+pat+sampling
    pat_build -g mpi gungho_model -o gungho_model+pat+mpi
    pat_build -g omp gungho_model -o gungho_model+pat+omp
    
    
fi