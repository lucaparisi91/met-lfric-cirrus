# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import PythonPackage


class CylcRose(PythonPackage):

    """Plugin providing support for Rose rose-suite.conf files."""

    homepage = "https://cylc.github.io/"
    pypi = "cylc-rose/cylc-rose-1.1.1.tar.gz"

    version(
        "1.2.0",
        sha256="a2410c1e761fdb61501e423410d814a543a0b3b59998ce8b700a46f6acc997ec",
    )
    version(
        "1.1.0",
        sha256="b7742970c388596d7d8eac499b41e4e51175688c8a5232927cc0b22d10e8242d",
    )
    version(
        "1.0.3",
        sha256="0e6f97c2e9b6192772b5c1f14f44f490d70319ceb92634485412e1dc54466dc3",
    )
    version(
        "1.0.2",
        sha256="0d1ac63eb3005a5d76011e13ea29e1b173788698e9365491e1ca6f296c02019c",
    )

    depends_on("python@3:")
    depends_on("py-setuptools")
