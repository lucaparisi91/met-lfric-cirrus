# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import CMakePackage


class Foxml(CMakePackage):

    """FoX - the Fortan/XML library.

    FoX is an XML library written in Fortran 95. It allows software
    developers to read, write and modify XML documents from Fortran
    applications without the complications of dealing with
    multi-language development. FoX can be freely redistributed as
    part of open source and commercial software packages.
    """

    homepage = "https://github.com/andreww/fox"
    url = "https://github.com/andreww/fox/tarball/6f60cf178d0776b21406303e91f1e6b42ff0f204"

    # -- this is for last commit March 4th 2021 rather than just latest "master"
    # version('6f60cf178d0776b21406303e91f1e6b42ff0f204', sha256='e44da2f2c39a18db7fa00a40d682f4e698d113581ec5935293089e7addd0afc2')
    version(
        "6f60cf1",
        sha256="e44da2f2c39a18db7fa00a40d682f4e698d113581ec5935293089e7addd0afc2",
    )
