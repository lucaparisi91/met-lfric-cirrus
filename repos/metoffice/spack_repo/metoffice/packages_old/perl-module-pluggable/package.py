# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import PerlPackage


class PerlModulePluggable(PerlPackage):

    """Module::Pluggable - automatically give your module the ability to have plugins.

    Why would you want to do this? Say you have something that wants
    to pass an object to a number of different plugins in turn. For
    example you may want to extract meta-data from every email you get
    sent and do something with it. Plugins make sense here because
    then you can keep adding new meta data parsers and all the logic
    and docs for each one will be self contained and new handlers are
    easy to add without changing the core code.
    """

    homepage = "https://metacpan.org/pod/Module::Pluggable"
    url = "https://cpan.metacpan.org/authors/id/S/SI/SIMONW/Module-Pluggable-5.2.tar.gz"

    version(
        "5.2", sha256="b3f2ad45e4fd10b3fb90d912d78d8b795ab295480db56dc64e86b9fa75c5a6df"
    )
