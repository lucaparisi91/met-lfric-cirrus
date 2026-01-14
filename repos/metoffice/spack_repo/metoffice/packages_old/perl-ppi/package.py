# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import PerlPackage


class PerlPpi(PerlPackage):

    """PPI - Parse, Analyze and Manipulate Perl (without perl)."""

    homepage = "https://metacpan.org/pod/PPI"
    url = "https://cpan.metacpan.org/authors/id/O/OA/OALDERS/PPI-1.276.tar.gz"

    version(
        "1.276",
        sha256="657655470e78b7c5b7660f7dec82893489c2e2d880e449135613da3b37500f01",
    )
