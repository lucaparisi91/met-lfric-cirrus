# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import PythonPackage


class MetomiRose(PythonPackage):

    """Rose - a framework for managing and running meteorological suites."""

    pypi = "metomi-rose/metomi-rose-2.0.2.tar.gz"

    version(
        "2.0.2",
        sha256="3a570172fe264766794ef063a5e56c547bd680e8c1b99325a432366b86e8936a",
    )
    version(
        "2.0.1",
        sha256="d720ee494490b43520ebe21c7a8e7ee13aba0ff30515ce407d6a4095e8428d93",
    )
    version(
        "2.0.0",
        sha256="12844b09c119b7f8e74e7b8f4f6d44a81ce5d399de820b2d415935af0b01da51",
    )
    version(
        "2.0rc3",
        sha256="9ff325e6d944bccee8d8cffa6530e25bf63824218b0b56751cdb51fe22295c51",
    )
    version(
        "2.0rc2",
        sha256="9b2c6396795c8849657edb584fa52db7c9cc1f6264b8e3c6df577524033c4f48",
    )

    depends_on("python@3:")
    depends_on("py-setuptools")
