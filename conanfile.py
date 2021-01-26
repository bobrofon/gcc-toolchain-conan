import os

from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration

required_conan_version = ">=1.32.0"


class GccToolchainConan(ConanFile):
    name = "gcc-toolchain"
    version = "6.3.0"
    license = "GPL-3.0-or-later"
    author = "Sergey Bobrenok <bobrofon@gmail.com>"
    url = "https://github.com/bobrofon/gcc-toolchain-conan"
    description = "Cross toolchain based on gcc compiler"
    topics = ("gcc", "cross-compile", "conan")
    settings = {"os": ["Linux"],
                "arch": ["x86_64"]}
    options = {"target": "ANY"}
    default_options = {"target": None}
    _source_subfolder = "source_subfolder"

    def _target(self, arch):
        targets = {
            "x86": "i686-unknown-linux-gnu",
            "x86_64": "x86_64-unknown-linux-gnu",
            "armv6": "arm-unknown-linux-gnueabi",
            "armv8": "aarch64-unknown-linux-gnueabi",
        }
        return targets.get(str(arch), None)

    def configure(self):
        settings_target = getattr(self, 'settings_target', None)
        if settings_target is None:
            if not self.options.target:
                raise ConanInvalidConfiguration("A value for option 'target' has to be provided")
        else:
            if self.options.target:
                raise ConanInvalidConfiguration("Value for the option 'target' will be computed from settings_target")
            if settings_target.os != "Linux":
                raise ConanInvalidConfiguration("Only Linux supported")
            if self._target(settings_target.arch) is None:
                raise ConanInvalidConfiguration("Arch is unsupported")
            self.options.target = settings_target.arch

    def source(self):
        tools.get(**self.conan_data["sources"]["armv6"])
        tools.get(**self.conan_data["sources"]["armv8"])
        tools.get(**self.conan_data["sources"]["x86"])
        tools.get(**self.conan_data["sources"]["x86_64"])

    def build(self):
        os.rename(self._target(self.options.target), self._source_subfolder)

    def package(self):
        self.copy("*", dst="", src=self._source_subfolder)

    def _define_tool_var(self, name, value):
        bin_path = os.path.join(self.package_folder, 'bin')
        triplet = self._target(self.options.target)
        file = "%s-%s" % (triplet, value)
        path = os.path.join(bin_path, file)
        self.output.info('Creating %s environment variable: %s' % (name, path))
        return path

    def package_info(self):
        bin_path = os.path.join(self.package_folder, "bin")
        self.output.info('Append PATH: %s' % bin_path)
        self.env_info.PATH.append(bin_path)

        triplet = self._target(self.options.target)
        self.output.info('Creating CHOST environment variable: %s' % triplet)
        self.env_info.CHOST = triplet

        sysroot = os.path.join(self.package_folder, triplet, "sysroot")
        self.output.info('Creating CONAN_CMAKE_FIND_ROOT_PATH environment variable: %s' % sysroot)
        self.env_info.CONAN_CMAKE_FIND_ROOT_PATH = sysroot

        self.output.info('Creating SYSROOT environment variable: %s' % sysroot)
        self.env_info.SYSROOT = sysroot

        self.output.info('Creating self.cpp_info.sysroot: %s' % sysroot)
        self.cpp_info.sysroot = sysroot

        self.env_info.CC = self._define_tool_var('CC', 'gcc')
        self.env_info.CXX = self._define_tool_var('CXX', 'g++')
        self.env_info.LD = self._define_tool_var('LD', 'ld')
        self.env_info.AR = self._define_tool_var('AR', 'ar')
        self.env_info.AS = self._define_tool_var('AS', 'as')
        self.env_info.RANLIB = self._define_tool_var('RANLIB', 'ranlib')
        self.env_info.STRIP = self._define_tool_var('STRIP', 'strip')
        self.env_info.ADDR2LINE = self._define_tool_var('ADDR2LINE', 'addr2line')
        self.env_info.NM = self._define_tool_var('NM', 'nm')
        self.env_info.OBJCOPY = self._define_tool_var('OBJCOPY', 'objcopy')
        self.env_info.OBJDUMP = self._define_tool_var('OBJDUMP', 'objdump')
        self.env_info.READELF = self._define_tool_var('READELF', 'readelf')
        self.env_info.ELFEDIT = self._define_tool_var('ELFEDIT', 'elfedit')

        self.env_info.CMAKE_FIND_ROOT_PATH_MODE_PROGRAM = "BOTH"
        self.env_info.CMAKE_FIND_ROOT_PATH_MODE_LIBRARY = "BOTH"
        self.env_info.CMAKE_FIND_ROOT_PATH_MODE_INCLUDE = "BOTH"
        self.env_info.CMAKE_FIND_ROOT_PATH_MODE_PACKAGE = "BOTH"
