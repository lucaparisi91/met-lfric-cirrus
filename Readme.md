
# Lfric on Cirrus-ex

This repo contains configuration and workflows for gungho benchmarks on cirrus-ex.

## Building the spack environment

```bash
module load spack
spack env activate environments/lfric
spack install
spack install
spack install
spack module lmod refresh --delete-tree -y
```


The build might fail the first time due to a quirk of yaxt, which fails at the first attempt, but succeeds at the second. You might need to call `spack install` several times, before succeeding.
You can load the lfric dependencies using 

```bash
module use $REPO_ROOT/environments/lfric/modules/Core
module load lfric-meta-spack-gcc/3.1.1
```

where REPO_ROOT is the folder containing a copy of this repo ( i.e. `/work/d435/d435/shared/lparisid435/met-lfric-cirrus`).
For examples of scripts to build lfric_apps see the `build_lfric` folder.