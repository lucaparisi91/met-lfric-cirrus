from spack_repo.builtin.packages.papi.package import Papi as PapiBase
import os


class Papi(PapiBase):

    @when("%cce")
    def patch(self):
        """Remove spurious GCC flags when using Cray CCE."""
        filter_file(
            r"FFLAGS=.*-ffixed-line-length-132.*",
            "true",
            os.path.join(os.getcwd(), "src", "configure.in"),
            backup=True,
        )
        filter_file(
            r"FFLAGS=.*-ffixed-line-length-132.*",
            "true",
            os.path.join(os.getcwd(), "src", "configure"),
            backup=True,
        )
        filter_file(
            r"-ffixed-line-length-132",
            "",
            os.path.join(os.getcwd(), "src", "ftests", "Makefile"),
            backup=True,
        )
