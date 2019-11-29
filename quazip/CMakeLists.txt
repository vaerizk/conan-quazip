set(QUAZIP_TARGET_NAME quazip)

set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_AUTOMOC ON)

find_package(Qt5 COMPONENTS
	Core
	REQUIRED
)
find_package(zlib REQUIRED)

file(GLOB QUAZIP_HEADERS LIST_DIRECTORIES=false *.h)
file(GLOB QUAZIP_SOURCES LIST_DIRECTORIES=false *.c *.cpp)

add_library(${QUAZIP_TARGET_NAME}
	${QUAZIP_HEADERS}
	${QUAZIP_SOURCES}
)

set_target_properties(${QUAZIP_TARGET_NAME} PROPERTIES
	DEBUG_POSTFIX d
)

target_include_directories(${QUAZIP_TARGET_NAME}
	PRIVATE
		${PROJECT_SOURCE_DIR}/quazip
	INTERFACE
		$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/quazip>
		# unqualified header paths taken from
		# quazip.pro : line 67
		# headers.path=$$PREFIX/include/quazip
		$<INSTALL_INTERFACE:include>
)

get_target_property(target_type ${QUAZIP_TARGET_NAME} TYPE)
if(target_type STREQUAL "STATIC_LIBRARY")
	target_compile_definitions(${QUAZIP_TARGET_NAME}
		PRIVATE
			QUAZIP_STATIC
	)
else()
	set_target_properties(${QUAZIP_TARGET_NAME} PROPERTIES
		DEFINE_SYMBOL QUAZIP_BUILD
	)
endif()

target_compile_options(${QUAZIP_TARGET_NAME}
	PRIVATE
		/W4
)

target_compile_definitions(${QUAZIP_TARGET_NAME}
	PRIVATE
		NOMINMAX # for win32 only
		QT_NO_CAST_FROM_ASCII
		QT_NO_CAST_TO_ASCII
)

target_link_libraries(${QUAZIP_TARGET_NAME}
	PUBLIC
		Qt5::Core
		ZLIB::ZLIB
)

# define installing rules for target files and associate them with an export
install(TARGETS ${QUAZIP_TARGET_NAME}
	EXPORT ${QUAZIP_EXPORT_NAME}
	ARCHIVE DESTINATION lib
	LIBRARY DESTINATION lib
	RUNTIME DESTINATION bin
)

install(FILES ${QUAZIP_HEADERS}
	# unqualified header paths taken from
	# quazip.pro : line 67
	# headers.path=$$PREFIX/include/quazip
	DESTINATION include
)

# group source files for IDE source explorers (e.g. Visual Studio)
source_group("Header Files" FILES
	${QUAZIP_HEADERS}	
)
source_group("Source Files" FILES
	${QUAZIP_SOURCES}
)
set_property(GLOBAL PROPERTY AUTOGEN_SOURCE_GROUP "Generated Files")
