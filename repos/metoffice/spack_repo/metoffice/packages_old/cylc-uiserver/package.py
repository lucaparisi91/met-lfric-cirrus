# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import PythonPackage


class CylcUiserver(PythonPackage):

    """Cylc UI server - provides the Cylc GUI."""

    homepage = "https://cylc.github.io/"
    pypi = "cylc-uiserver/cylc-uiserver-1.1.0.tar.gz"

    version(
        "1.2.0",
        sha256="0a5ceab75ce83f8e0a83148fe9de084ff32c75be372427d708b31fb44d9ed87c",
    )
    version(
        "1.1.0",
        sha256="f6d58085c9d8f3a6d4241343335371a9588cf667447a2c84b420eebee6bae5f5",
    )
    version(
        "1.0.3",
        sha256="a94560102656dc5e637b839139590403ee30e1e4abb61446cbdc5bfd33a3efb5",
    )
    version(
        "1.0.2",
        sha256="3a2510808873afcf7a0fd57766a7a203c9741b7afd485ab1c80da3d3bbb77e31",
    )
    version(
        "1.0.1",
        sha256="4ee50d2130adff797494c47a12881bd2b6e3afcf610a2d214c180e13f77e5818",
    )

    depends_on("python@3:")
    depends_on("py-setuptools")
