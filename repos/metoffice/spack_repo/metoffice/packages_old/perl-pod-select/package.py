# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import PerlPackage


class PerlPodSelect(PerlPackage):

    """Pod::Select() - extract selected sections of POD from input.

    podselect() is a function which will extract specified sections of
    pod documentation from an input stream. This ability is provided
    by the Pod::Select module which is a subclass of
    Pod::Parser. Pod::Select provides a method named select() to
    specify the set of POD sections to select for
    processing/printing. podselect() merely creates a Pod::Select
    object and then invokes the podselect() followed by
    parse_from_file().

    NOTE: This module is considered legacy; modern Perl releases
    (5.31.1 and higher) are going to remove Pod-Parser from core and
    use Pod::Simple for all things POD.
    """

    homepage = "https://metacpan.org/pod/Pod::Select"
    url = "https://cpan.metacpan.org/authors/id/M/MA/MAREKR/Pod-Parser-1.65.tar.gz"

    version(
        "1.65",
        sha256="3ba7bdec659416a51fe2a7e59f0883e9c6a3b21bc9d001042c1d6a32d401b28a",
    )
