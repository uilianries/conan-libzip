#!/usr/bin/python

# conanfile for build libzip (chosen because it only depends on zlib)

from conans import ConanFile, CMake, tools

import os


class LibZipConan(ConanFile):
  name = 'libzip'
  version = '1.2.0'
  license = 'bsd'
  url = 'https://github.com/k0ekk0ek/conan-libzip'
  generators = 'cmake', 'txt'
  settings = 'os', 'compiler', 'build_type', 'arch'
  options = {'shared': [True, False]}
  default_options = 'shared=True'

  # Convenience properties not required by Conan
  directory = '{}-{}'.format(name, version)
  filename = '{}.tar.gz'.format(directory)
  checksum = '6cf9840e427db96ebf3936665430bab204c9ebbd0120c326459077ed9c907d9f'

  def source(self):
    tools.download(
      'https://nih.at/libzip/{}'.format(self.filename), self.filename)
    tools.check_sha256(self.filename, self.checksum)
    tools.unzip(self.filename, '.')
    os.unlink(self.filename)
  # source

  def configure(self):
    self.requires.add("zlib/1.2.11@conan/stable", private=False)
    self.options['zlib'].shared = self.options.shared
  # configure

  def build(self):
    # Add inclusion of conanbuildinfo.cmake otherwise libzip will use the
    # version of zlib shipped with the platform
    cmakelists = '{}/CMakeLists.txt'.format(self.directory)
    search = 'CMAKE_MINIMUM_REQUIRED(VERSION 2.6)'
    replace = '''PROJECT(libzip C)
CMAKE_MINIMUM_REQUIRED(VERSION 3.0)
include(../conanbuildinfo.cmake)
CONAN_BASIC_SETUP()
'''

    tools.replace_in_file(cmakelists, search, replace)

    # Update libzip-x.x/lib/CMakeLists.txt to enable creating a static library
    # FIXME: implement

    # Build the sources using CMake
    cmake = CMake(self)
    self.run('cmake {} {}'.format(self.directory, cmake.command_line))
    self.run('cmake --build . {}'.format(cmake.build_config))
  # build

  def package(self):
    # Header files
    self.copy('zip.h', dst='include',  src=self.directory, keep_path=False)
    self.copy('zipconf.h', dst='include', keep_path=False)
    self.copy('config.h', dst='include/libzip', keep_path=False)
    # Libraries
    self.copy('*.lib', dst='lib', keep_path=False)
    self.copy('*.dll', dst='bin', keep_path=False)
    if self.options.shared:
      self.copy('*.so', dst='lib', keep_path=False)
    self.copy('*.a', dst='lib', keep_path=False)
  # package

