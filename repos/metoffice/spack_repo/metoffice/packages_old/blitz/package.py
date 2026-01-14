# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.packages.blitz.package import Blitz as BaseBlitz


class Blitz(BaseBlitz):

    """N-dimensional arrays for C++"""

    version(
        "1.0.1",
        sha256="b62fc3f07b64b264307b01fec5e4f2793e09a68dcb5378984aedbc2e4b3adcef",
    )
    version(
        "1.0.0",
        sha256="79c06ea9a0585ba0e290c8140300e3ad19491c45c1d90feb52819abc3b58a0c1",
    )

    depends_on("python@:2.7", type="build", when="@:1.0.1")
    depends_on("python@3:", type="build", when="@1.0.2:")
    depends_on("papi@:5.7", type="link")

    def patch(self):

        """Fix compiler vendor detection macros.

        Compiler vendor detection is broken on the Cray EX.  This adds
        a default to the m4 definition to target llvm when using a
        recent version of cce.
        """

        if "%cce" in self.spec and self.compiler.version >= ver(15):
            # Add a default compiler vendor and set it to llvm if
            # using a recent Cray compiler
            filter_file("^\)", "[COMPILER_VENDOR=\"llvm\"]\n)",
                        "m4/ac_compiler_specific_header.m4")
