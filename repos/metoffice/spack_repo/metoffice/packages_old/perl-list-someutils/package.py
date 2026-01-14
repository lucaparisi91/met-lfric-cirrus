# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import PerlPackage


class PerlListSomeutils(PerlPackage):

    """List::SomeUtils - Provide the stuff missing in List::Util.

    List::SomeUtils provides some trivial but commonly needed
    functionality on lists which is not going to go into List::Util.

    All of the below functions are implementable in only a couple of
    lines of Perl code. Using the functions from this module however
    should give slightly better performance as everything is
    implemented in C. The pure-Perl implementation of these functions
    only serves as a fallback in case the C portions of this module
    couldn't be compiled on this machine.
    """

    homepage = "https://metacpan.org/pod/List::SomeUtils"
    url = "https://cpan.metacpan.org/authors/id/D/DR/DROLSKY/List-SomeUtils-0.59.tar.gz"

    version(
        "0.59",
        sha256="fab30372e4c67bf5a46062da38d1d0c8756279feada866eb439fa29571a2dc7b",
    )
