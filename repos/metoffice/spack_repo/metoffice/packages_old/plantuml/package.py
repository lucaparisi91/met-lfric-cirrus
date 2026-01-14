# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# ----------------------------------------------------------------------------
from textwrap import dedent
from spack_repo.builtin.build_systems.generic import Package
from spack.package import *


class Plantuml(Package):
    """
    Renders UML diagrams from textual descriptions.
    """
    homepage = "https://github.com/plantuml/plantuml"

    # notify when the package is updated.
    maintainers("andrewcoughtrie", "t00sa", "MatthewHambley")

    # See https://spdx.org/licenses/ for a list. Upon manually verifying
    # the license, set checked_by to your Github username.
    license("BSD-3-Clause", checked_by="MatthewHambley")

    version("1.2025.0", expand=False,
            sha256="973d65b135377e2a1a8c0de59f4b69b699f1807674069cad7b9f8bff0030f6b7")
    version("1.2024.5", expand=False,
            sha256="c3230b9ee0a9ea70c53b9d9bae13acee0854ebb26371b0d930b35d19525fa143")

    depends_on("java", type="run")
    depends_on("graphviz+expat", type="run")

    def url_for_version(self, version: Version):
        url_root = "https://github.com/plantuml/plantuml/releases/download"
        return f"{url_root}/v{version}/plantuml-bsd-{version}.jar"

    def install(self, spec, prefix):
        bin_path = Path(prefix.bin)
        bin_path.mkdir(parents=True)

        install(self.stage.archive_file, prefix.bin)
        jar_file = bin_path / Path(self.stage.archive_file).name

        script_file = bin_path / 'plantuml'
        script_file.write_text(
            dedent(
                f"""
                #!/bin/sh
                java -jar {str(jar_file)} $*
                """
            ).lstrip()
        )
        script_file.chmod(0o755)
