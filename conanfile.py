#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
from conans.errors import ConanException
from conans.model.version import Version
import os


class BenchmarkConan(ConanFile):
    name = "benchmark"
    version = "1.4.1"
    description = "A microbenchmark support library"
    url = "https://github.com/bincrafters/conan-benchmark"
    homepage = "https://github.com/google/benchmark"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "Apache-2.0"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "exceptions": [True, False],
        "lto": [True, False],
    }

    default_options = "shared=False", "fPIC=True", "exceptions=True", "lto=False"

    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC
            del self.options.shared

    def source(self):
        source_url = self.homepage
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version

        os.rename(extracted_dir, self.source_subfolder)

    def configure(self):
        if self.settings.compiler == "gcc":
            if Version(self.settings.compiler.version.value) < "4.8":
                raise ConanException("g++ >= 4.8 is required, yours is %s" % self.settings.compiler.version)
        if self.settings.compiler == "clang" and Version(self.settings.compiler.version.value) < "3.4":
            raise ConanException("clang >= 3.4 is required, yours is %s" % self.settings.compiler.version)
        if self.settings.compiler == "Visual Studio" and Version(self.settings.compiler.version.value) < "12":
            raise ConanException("Visual Studio >= 12 is required, yours is %s" % self.settings.compiler.version)

    def configure_cmake(self):
        cmake = CMake(self)
        if self.settings.os != 'Windows':
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        if self.settings.compiler in ['clang', 'apple-clang']:
            cmake.definitions['BENCHMARK_USE_LIBCXX'] = self.settings.compiler.libcxx == 'libc++'
        cmake.definitions['BENCHMARK_ENABLE_TESTING'] = False
        cmake.definitions['BENCHMARK_ENABLE_EXCEPTIONS'] = self.options.exceptions
        cmake.definitions['BENCHMARK_ENABLE_LTO'] = self.options.lto
        cmake.configure(build_folder=self.build_subfolder)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self.source_subfolder)
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ['benchmark_main', 'benchmark']

        if self.settings.os == 'Linux':
            self.cpp_info.libs.append('pthread')
        elif self.settings.os == 'Windows':
            self.cpp_info.libs.append('Shlwapi.lib')
