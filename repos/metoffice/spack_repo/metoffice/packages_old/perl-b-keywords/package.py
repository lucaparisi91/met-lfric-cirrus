# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import PerlPackage


class PerlBKeywords(PerlPackage):

    """B::Keywords - Lists of reserved barewords and symbol names."""

    homepage = "https://metacpan.org/pod/B::Keywords"
    url = "https://cpan.metacpan.org/authors/id/R/RU/RURBAN/B-Keywords-1.24.tar.gz"

    version(
        "1.24",
        sha256="a5cf6bb285d06d17cee227783b723bb274213fd4153a5dee311d240e1169606e",
    )
