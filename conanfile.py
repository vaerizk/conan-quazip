from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
import os.path
import shutil


class QuaZipConan(ConanFile):
    name = "quazip"
    version="0.8.1"
    license = "LGPL-2.1, zlib/png"
    url = "https://github.com/vaerizk/quazip"
    homepage = "https://github.com/stachenov/quazip"
    description = "A C++ wrapper for Gilles Vollant's ZIP/UNZIP package (AKA Minizip) using Qt library"
    topics = ("quazip", "conan-recipe")

    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {
        "shared": True,
        "zlib:shared": False
    }

    revision_mode = "scm"

    generators = "cmake_paths"
    exports_sources = [
        "CMakeLists.txt",
        os.path.join("quazip", "CMakeLists.txt"),
        os.path.join("cmake", "quazip-config.cmake.in")
    ]
    no_copy_source = True

    _source_subdir_name = "source_subdir"

    def configure(self):
        if self.settings.os != "Windows":
            raise ConanInvalidConfiguration("Only windows is supported at the moment")

    def build_requirements(self):
        self.build_requires("cmake/[>3.0.0]")

    def requirements(self):
        self.requires("qt/[5.12.7]@bincrafters/stable", private=False)
        self.requires("zlib/1.2.11", private=False)

    def source(self):
        url = "https://github.com/stachenov/quazip/archive/v{}.zip".format(self.version)
        tools.get(url)
        os.rename("quazip-{}".format(self.version), self._source_subdir_name)

        # replace CMakeLists
        os.rename(
            os.path.join(self._source_subdir_name, "CMakeLists.txt"),
            os.path.join(self._source_subdir_name, "CMakeLists-original.txt")
        )
        shutil.copy("CMakeLists.txt", os.path.join(self._source_subdir_name, "CMakeLists.txt"))
        os.rename(
            os.path.join(self._source_subdir_name, "quazip", "CMakeLists.txt"),
            os.path.join(self._source_subdir_name, "quazip", "CMakeLists-original.txt")
        )
        shutil.copy(os.path.join("quazip", "CMakeLists.txt"), os.path.join(self._source_subdir_name, "quazip", "CMakeLists.txt"))

        os.mkdir(os.path.join(self._source_subdir_name, "cmake"))
        shutil.copy(os.path.join("cmake", "quazip-config.cmake.in"), os.path.join(self._source_subdir_name, "cmake"))

    def build(self):
        cmake = CMake(self)
        cmake.definitions["VERSION"] = self.version
        cmake.definitions["CMAKE_TOOLCHAIN_FILE"] = os.path.join(self.build_folder, "conan_paths.cmake")
        cmake.configure(source_folder=self._source_subdir_name)
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self._source_subdir_name)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
