# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import PerlPackage


class PerlPpixRegexp(PerlPackage):

    """PPIx::Regexp - Represent a regular expression of some sort.

    The purpose of the PPIx-Regexp package is to parse regular
    expressions in a manner similar to the way the PPI package parses
    Perl. This class forms the root of the parse tree, playing a role
    similar to PPI::Document.
    """

    homepage = "https://metacpan.org/pod/PPIx::Regexp"
    url = "https://cpan.metacpan.org/authors/id/W/WY/WYANT/PPIx-Regexp-0.086.tar.gz"

    version(
        "0.086",
        sha256="36bd2dfdf321394d11433fa3eec76c70b7fc4625bd1209316395a2c895dc3933",
    )
