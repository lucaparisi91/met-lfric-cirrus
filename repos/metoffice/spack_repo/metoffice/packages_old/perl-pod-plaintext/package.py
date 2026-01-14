# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import PerlPackage


class PerlPodPlaintext(PerlPackage):

    """Pod::PlainText - Convert POD data to formatted ASCII text.

    Pod::PlainText is a module that can convert documentation in the
    POD format (the preferred language for documenting Perl) into
    formatted ASCII. It uses no special formatting controls or codes
    whatsoever, and its output is therefore suitable for nearly any
    device.
    """

    homepage = "https://metacpan.org/pod/Pod::PlainText"
    url = "https://cpan.metacpan.org/authors/id/M/MA/MAREKR/Pod-Parser-1.65.tar.gz"

    version(
        "1.65",
        sha256="3ba7bdec659416a51fe2a7e59f0883e9c6a3b21bc9d001042c1d6a32d401b28a",
    )
