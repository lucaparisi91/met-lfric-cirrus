# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import PerlPackage


class PerlPodSpell(PerlPackage):

    """Pod::Spell - a formatter for spellchecking Pod.

    Pod::Spell is a Pod formatter whose output is good for
    spellchecking. Pod::Spell is rather like Pod::Text, except that it
    doesn't put much effort into actual formatting, and it suppresses
    things that look like Perl symbols or Perl jargon (so that your
    spellchecking program won't complain about mystery words like
    "$thing" or "Foo::Bar" or "hashref").
    """

    homepage = "https://metacpan.org/pod/Pod::Spell"
    url = "https://cpan.metacpan.org/authors/id/H/HA/HAARG/Pod-Spell-1.25.tar.gz"

    version(
        "1.25",
        sha256="208f8e8b9bc9bd312a6bb2c474f49c1ab568894990dff49035fcc234acbb9fa3",
    )

    depends_on("perl-file-sharedir-install", type=("build", "run"))
