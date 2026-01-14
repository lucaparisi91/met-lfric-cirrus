# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import PythonPackage


class CylcFlow(PythonPackage):

    """Cylc - workflow engine that orchestrates cycling workflows very efficiently.

    Cylc is used in production weather, climate, and environmental
    forecasting on HPC, but is not specialized to those domains.
    """

    homepage = "https://cylc.github.io/"
    pypi = "cylc-flow/cylc-flow-8.0.4.tar.gz"

    version(
        "8.1.0",
        sha256="19e1e510178d2ea6210bbd5e56dbe30c5066665564b46a6faad134dede831487",
    )
    version(
        "8.0.4",
        sha256="866f39bec037805690ce582a2cb0ccdbf646ea46a4c691c9cb1a1ea13f649a7a",
    )
    version(
        "8.0.1",
        sha256="dfccc1290390f226fe44253bcb0caf65aa175e2f7d165793083feed1f8ea0a7f",
    )
    version(
        "8.0.0",
        sha256="5a4b4bb4e101d65c5c397e6ab810d21b90c8774dca3a9e708de96b22e43d0cfe",
    )
    version(
        "8.0rc2",
        sha256="a8887fcf8f014e2665c9ebbe8a596a71e383e23859fa485860469b7f59fafd2f",
    )

    depends_on("python@3:")
    depends_on("py-setuptools")
    depends_on("graphviz")
