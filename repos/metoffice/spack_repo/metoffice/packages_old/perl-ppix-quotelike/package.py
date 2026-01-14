# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import PerlPackage


class PerlPpixQuotelike(PerlPackage):

    """PPIx::QuoteLike - Parse Perl string literals and string-literal-like things.

    This Perl class parses Perl string literals and things that are
    reasonably like string literals. Its real reason for being is to
    find interpolated variables for Perl::Critic policies and similar
    code.
    """

    homepage = "https://metacpan.org/pod/PPIx::QuoteLike"
    url = "https://cpan.metacpan.org/authors/id/W/WY/WYANT/PPIx-QuoteLike-0.023.tar.gz"

    version(
        "0.023",
        sha256="3576a3149d2c53e07e9737b7892be5cfb84a499a6ef1df090b713b0544234d21",
    )
