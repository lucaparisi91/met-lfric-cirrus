# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import PerlPackage


class PerlPpixUtilities(PerlPackage):

    """PPIx::Utilities - Extensions to PPI.

    This is a collection of functions for dealing with PPI objects,
    many of which originated in Perl::Critic. They are organized into
    modules by the kind of PPI class they relate to, by replacing the
    "PPI" at the front of the module name with "PPIx::Utilities",
    e.g. functionality related to PPI::Nodes is in
    PPIx::Utilities::Node.
    """

    homepage = "https://metacpan.org/pod/PPIx::Utilities"
    url = "https://cpan.metacpan.org/authors/id/E/EL/ELLIOTJS/PPIx-Utilities-1.001000.tar.gz"

    version(
        "1.001000",
        sha256="03a483386fd6a2c808f09778d44db06b02c3140fb24ba4bf12f851f46d3bcb9b",
    )
