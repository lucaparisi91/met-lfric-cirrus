# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from curses import version

from spack_repo.builtin.build_systems.bundle import BundlePackage
from spack.package import *

class LfricMeta(BundlePackage):
    """Dependencies of LFRic."""

    version("1.2")
    version("2.0")
    version("2.1")
    version("2.2")
    version("3.0")
    version("3.1.0")
    version("3.1.1")

    # Dependencies
    depends_on("mpi", type="run")
    depends_on("hdf5+mpi",type = "run")
    depends_on("netcdf-c+mpi", type="run")
    depends_on("netcdf-fortran", type="run")
    depends_on("yaxt", type="run")
    depends_on("py-jinja2", type="run")
    depends_on("py-psyclone@2.5.0", when='@:1.2', type="run")
    depends_on("py-psyclone@3.0.0", when='@2.0', type="run")
    depends_on("py-psyclone@3.1.0", when='@2.1:3.1.0', type="run")
    depends_on("py-psyclone@3.2.2", when='@3.1.1:', type="run")
    depends_on("py-pyyaml",when='@3.0:', type="run") 
    depends_on("rose-picker", type="run")
    depends_on("xios@2701", type="run")
    depends_on("shumlib@13.0+openmp", type="run")
    # depends_on("pfunit@3.2.9")
    
    depends_on("cxx", type='build')
    depends_on("c", type='build')
    depends_on("fortran", type='build')
    
    
    # Set up environment paths
    def setup_run_environment(self, run_env):
        spec = self.spec

        # Compiler agnostic env vars
        run_env.set("FC", "ftn")
        run_env.set("LDMPI", "ftn")
        run_env.set("FPP", "cpp -traditional-cpp")
