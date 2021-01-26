#!/usr/bin/env python3

from cpt.packager import ConanMultiPackager

if __name__ == "__main__":
    settings = {
        "os": "Linux",
        "os_build": "Linux",
        "arch": "x86_64",
        "arch_build": "x86_64",
        "compiler": "gcc",
        "compiler.version": 6,
        "compiler.libcxx": "libstdc++11",
        "compiler.cppstd": 14,
        "build_type": "Release",
    }

    builder = ConanMultiPackager()
    builder.add(settings=settings, options={"gcc-toolchain:target": "armv6"})
    builder.add(settings=settings, options={"gcc-toolchain:target": "armv8"})
    builder.add(settings=settings, options={"gcc-toolchain:target": "x86"})
    builder.add(settings=settings, options={"gcc-toolchain:target": "x86_64"})
    builder.run()
