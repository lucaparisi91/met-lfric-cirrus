# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import PerlPackage


class PerlFileWhich(PerlPackage):

    """File::Which - Perl implementation of the which utility as an API.

    File::Which finds the full or relative paths to executable
    programs on the system. This is normally the function of which
    utility. which is typically implemented as either a program or a
    built in shell command. On some platforms, such as Microsoft
    Windows it is not provided as part of the core operating
    system. This module provides a consistent API to this
    functionality regardless of the underlying platform.

    The focus of this module is correctness and portability. As a
    consequence platforms where the current directory is implicitly
    part of the search path such as Microsoft Windows will find
    executables in the current directory, whereas on platforms such as
    UNIX where this is not the case executables in the current
    directory will only be found if the current directory is
    explicitly added to the path.

    If you need a portable which on the command line in an environment
    that does not provide it, install App::pwhich which provides a
    command line interface to this API.
    """

    homepage = "https://metacpan.org/pod/File::Which"
    url = "https://cpan.metacpan.org/authors/id/P/PL/PLICEASE/File-Which-1.27.tar.gz"

    version(
        "1.27",
        sha256="3201f1a60e3f16484082e6045c896842261fc345de9fb2e620fd2a2c7af3a93a",
    )
