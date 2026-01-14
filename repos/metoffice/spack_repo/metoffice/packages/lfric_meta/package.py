# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.bundle import BundlePackage
from spack.package import *

class LfricMeta(BundlePackage):
    """Dependencies of LFRic."""

    version("1.2")
    version("2.0")
    version("2.1")
    version("2.2")

    # Dependencies
    depends_on("mpi")
    depends_on("hdf5+mpi")
    depends_on("netcdf-c+mpi")
    depends_on("netcdf-fortran")

    depends_on("yaxt")
    depends_on("py-jinja2")
    depends_on("py-psyclone@2.5.0", when='@:1.2')
    depends_on("py-psyclone@3.0.0", when='@2.0')
    depends_on("py-psyclone@3.1.0", when='@2.1:')
    depends_on("rose-picker")
    depends_on("xios@2.6")
    # depends_on("pfunit@3.2.9")

    # Set up environment paths
    def setup_run_environment(self, run_env):
        spec = self.spec

        # Compiler agnostic env vars
        run_env.set("FC", "ftn")
        run_env.set("LDMPI", "ftn")
        run_env.set("FPP", "cpp -traditional-cpp")
