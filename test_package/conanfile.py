from conans import ConanFile, tools


class GccToolchainTestConan(ConanFile):
    settings = "os", "arch"

    def build(self):
        pass

    def test(self):
        if not tools.cross_building(self):
            self.run("$CC --version", run_environment=True)
