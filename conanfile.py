#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class LibZipConan(ConanFile):
    name = "libzip"
    description = "A C library for reading, creating, and modifying zip archives"
    version = "1.5.1"
    url = "https://github.com/bincrafters/conan-libzip"
    homepage = "https://github.com/nih-at/libzip"
    license = "BSD"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "with_bzip2": [True, False]}
    default_options = "shared=False", "with_bzip2=True"
    requires = "zlib/1.2.11@conan/stable"

    def source(self):
        source_url = "https://libzip.org/download"
        tools.get("{0}/{1}-{2}.tar.gz".format(source_url, self.name, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def requirements(self):
        if self.options.with_bzip2:
            self.requires.add("bzip2/1.0.6@conan/stable")

        if self.settings.os == "Windows" or self.settings.os == "Linux":
            self.requires("OpenSSL/[>=1.0]@conan/stable")

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.configure()
        return cmake

    def exclude_targets(self):
        excluded_targets = ["regress", "examples", "man"]
        for target in excluded_targets:
            tools.replace_in_file(os.path.join(self.source_subfolder, "CMakeLists.txt"), "ADD_SUBDIRECTORY(%s)" % target, "")

    def build(self):
        self.exclude_targets()
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()
        self.copy(pattern="LICENSE", dst="licenses", src=self.source_subfolder)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
