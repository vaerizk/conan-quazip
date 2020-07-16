from conans import ConanFile, CMake, tools
import os


class QuaZipTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake_paths"

    @property
    def _bin_dir(self):
        cmake = CMake(self)
        if cmake.is_multi_configuration:
            return str(self.settings.build_type)
        return "."

    def build_requirements(self):
        self.build_requires("cmake_installer/[>3.0.0]@conan/stable")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["CMAKE_TOOLCHAIN_FILE"] = os.path.join(self.build_folder, "conan_paths.cmake")
        cmake.configure()
        cmake.build()

    def test(self):
        if not tools.cross_building(self.settings):
            self.run(os.path.join(self._bin_dir, "test_package"), run_environment=True)
