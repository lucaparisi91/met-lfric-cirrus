# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import PerlPackage


class PerlTidy(PerlPackage):

    """Perl::Tidy - Parses and beautifies perl source.

    This module makes the functionality of the perltidy utility
    available to perl scripts. Any or all of the input parameters may
    be omitted, in which case the @ARGV array will be used to provide
    input parameters as described in the perltidy(1) man page.
    """

    homepage = "https://metacpan.org/pod/Perl::Tidy"
    url = "https://cpan.metacpan.org/authors/id/S/SH/SHANCOCK/Perl-Tidy-20221112.tar.gz"

    version(
        "20221112",
        sha256="8e3fffbaadb5612ff2c66742641838cf403ff1ed11091f5f5d72a8eb61c4bfa8",
    )
