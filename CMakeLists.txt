cmake_minimum_required(VERSION 3.0)

project(quazip VERSION ${VERSION} LANGUAGES C CXX)

# project variables
set(QUAZIP_PACKAGE_NAME ${PROJECT_NAME})
set(QUAZIP_EXPORT_NAME ${QUAZIP_PACKAGE_NAME}-targets)
set(QUAZIP_CONFIG_FILENAME ${QUAZIP_PACKAGE_NAME}-config.cmake)
set(QUAZIP_CONFIGVERSION_FILENAME ${QUAZIP_PACKAGE_NAME}-config-version.cmake)
set(QUAZIP_CMAKE_DIR cmake)

add_subdirectory(quazip)

# generate config file
configure_file(
	"${QUAZIP_CMAKE_DIR}/${QUAZIP_CONFIG_FILENAME}.in"
	"${QUAZIP_CMAKE_DIR}/${QUAZIP_CONFIG_FILENAME}"
	@ONLY
)

include(CMakePackageConfigHelpers)
write_basic_package_version_file("${QUAZIP_CMAKE_DIR}/${QUAZIP_CONFIGVERSION_FILENAME}"
	COMPATIBILITY SameMinorVersion # TODO: when quazip is released compatibility should be revised
)

# install config and config-version files
install(FILES
	"${PROJECT_BINARY_DIR}/${QUAZIP_CMAKE_DIR}/${QUAZIP_CONFIG_FILENAME}"
	"${PROJECT_BINARY_DIR}/${QUAZIP_CMAKE_DIR}/${QUAZIP_CONFIGVERSION_FILENAME}"
	DESTINATION "lib/${QUAZIP_CMAKE_DIR}/${QUAZIP_PACKAGE_NAME}"
)
# export targets from an installation tree
install(EXPORT ${QUAZIP_EXPORT_NAME}
	DESTINATION "lib/${QUAZIP_CMAKE_DIR}/${QUAZIP_PACKAGE_NAME}"
)

install(FILES "COPYING"
	DESTINATION licenses
)

# export targets from a build tree
export(EXPORT ${QUAZIP_EXPORT_NAME} FILE "${QUAZIP_CMAKE_DIR}/${QUAZIP_EXPORT_NAME}.cmake")
