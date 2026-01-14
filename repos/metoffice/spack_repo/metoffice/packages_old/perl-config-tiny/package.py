# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import PerlPackage


class PerlConfigTiny(PerlPackage):

    """Config::Tiny - Read/Write .ini style files with as little code as possible.

    Config::Tiny is a Perl class to read and write .ini style
    configuration files with as little code as possible, reducing load
    time and memory overhead.

    Most of the time it is accepted that Perl applications use a lot
    of memory and modules.

    The *::Tiny family of modules is specifically intended to provide
    an ultralight alternative to the standard modules.

    This module is primarily for reading human written files, and
    anything we write shouldn't need to have
    documentation/comments. If you need something with more power move
    up to Config::Simple, Config::General or one of the many other
    Config::* modules.

    Lastly, Config::Tiny does not preserve your comments, whitespace,
    or the order of your config file.

    See Config::Tiny::Ordered (and possibly others) for the
    preservation of the order of the entries in the file.
    """

    homepage = "https://metacpan.org/pod/Config::Tiny"
    url = "https://cpan.metacpan.org/authors/id/R/RS/RSAVAGE/Config-Tiny-2.28.tgz"

    version(
        "2.28",
        sha256="12df843a0d29d48f61bcc14c4f18f0858fd27a8dd829a00319529d654fe01500",
    )
