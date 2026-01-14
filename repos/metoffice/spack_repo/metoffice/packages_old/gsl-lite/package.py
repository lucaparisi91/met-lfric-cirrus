# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import CMakePackage


class GslLite(CMakePackage):

    """gsl-lite.

    A single-file header-only implementation of the C++ Core
    Guidelines Support Library originally based on Microsoft GSL and
    adapted for C++98, C++03. It also works when compiled as C++11,
    C++14, C++17, C++20.
    """

    homepage = "https://github.com/gsl-lite/gsl-lite"
    url = "https://github.com/gsl-lite/gsl-lite/archive/refs/tags/v0.34.0.tar.gz"

    version(
        "0.40.0",
        sha256="65af4ec8a1050dac4f1ca4622881bb02a9c3978a9baec289fb56e25412d6cac7",
    )
    version(
        "0.39.0",
        sha256="f80ec07d9f4946097a1e2554e19cee4b55b70b45d59e03a7d2b7f80d71e467e9",
    )
    version(
        "0.38.1",
        sha256="c2fa2315fff312f3897958903ed4d4e027f73fa44235459ecb467ad7b7d62b18",
    )
    version(
        "0.38.0",
        sha256="5d25fcd31ea66dac9e14da1cad501d95450ccfcb2768fffcd1a4170258fcbc81",
    )
    version(
        "0.37.0",
        sha256="a31d51b73742bb234acab8d2411223cf299e760ed713f0840ffed0dabe57ca38",
    )
    version(
        "0.36.0",
        sha256="c052cc4547b33cedee6f000393a7005915c45c6c06b35518d203db117f75c71c",
    )
    version(
        "0.34.0",
        sha256="a7d5b2672b78704ca03df9ef65bc274d8f8cacad3ca950365eef9e25b50324c5",
    )
    version(
        "0.33.0",
        sha256="ebbbfa28656fb43356dceec90663f8398d2cb0c583ebaf32c8a385d5efd0bbca",
    )
    version(
        "0.32.0",
        sha256="134c891b0b0f038d622554faa4040f6d419c534ed18c1b893f4f3ff788515d10",
    )
