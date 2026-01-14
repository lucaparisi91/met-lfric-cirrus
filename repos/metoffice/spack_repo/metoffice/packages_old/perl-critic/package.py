# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import PerlPackage


class PerlCritic(PerlPackage):

    """Critic - Critique Perl source code for best-practices.

    Perl::Critic is an extensible framework for creating and applying
    coding standards to Perl source code. Essentially, it is a static
    source code analysis engine. Perl::Critic is distributed with a
    number of Perl::Critic::Policy modules that attempt to enforce
    various coding guidelines.

    Most Policy modules are based on Damian Conway's book Perl Best
    Practices. However, Perl::Critic is not limited to PBP and will
    even support Policies that contradict Conway. You can enable,
    disable, and customize those Polices through the Perl::Critic
    interface. You can also create new Policy modules that suit your
    own tastes.
    """

    homepage = "https://metacpan.org/pod/Perl::Critic"
    url = "https://cpan.metacpan.org/authors/id/P/PE/PETDANCE/Perl-Critic-1.148.tar.gz"

    version(
        "1.148",
        sha256="cf8a5cdc66f9bd40eb516396213f65227eac4b5fa035d4353ace9b3c329e1096",
    )

    depends_on("perl")

    depends_on("perl-b-keywords", type=("build", "run"))
    depends_on("perl-clone", type=("build", "run"))
    depends_on("perl-config-tiny", type=("build", "run"))
    depends_on("perl-exception-class", type=("build", "run"))
    depends_on("perl-extutils-makemaker", type=("build", "run"))
    depends_on("perl-file-which", type=("build", "run"))
    depends_on("perl-list-someutils", type=("build", "run"))
    depends_on("perl-module-build", type=("build", "run"))
    depends_on("perl-module-implementation", type=("build", "run"))
    depends_on("perl-module-pluggable", type=("build", "run"))
    depends_on("perl-params-util", type=("build", "run"))
    depends_on("perl-ppi", type=("build", "run"))
    depends_on("perl-ppix-quotelike", type=("build", "run"))
    depends_on("perl-ppix-regexp", type=("build", "run"))
    depends_on("perl-ppix-utilities", type=("build", "run"))
    depends_on("perl-pod-plaintext", type=("build", "run"))
    depends_on("perl-pod-select", type=("build", "run"))
    depends_on("perl-pod-spell", type=("build", "run"))
    depends_on("perl-readonly", type=("build", "run"))
    depends_on("perl-string-format", type=("build", "run"))
    depends_on("perl-test-more", type=("build", "run"))
    depends_on("perl-tidy", type=("build", "run"))
