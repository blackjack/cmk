cmake_minimum_required (VERSION 2.8.11)
project (cmk)


set (CMAKE_EXPORT_COMPILE_COMMANDS 1)
set (CMAKE_CXX_STANDARD 14)


set (INPUT_YAML
  inputs/test1.yaml
  )

add_custom_command(
  OUTPUT outputs/generated.timestamp

  COMMAND
  python ${CMAKE_CURRENT_SOURCE_DIR}/autogen.py
  --input-dir ${CMAKE_CURRENT_SOURCE_DIR}/inputs
  --output-dir ${CMAKE_BINARY_DIR}/outputs
  --cmake ${CMAKE_BINARY_DIR}/outputs/generated_srcs.cmake

  COMMAND touch ${CMAKE_BINARY_DIR}/outputs/generated.timestamp

  DEPENDS autogen.py
  DEPENDS ${INPUT_YAML}
  COMMENT "Running autogen"
  VERBATIM
  )

add_custom_target(
  autogen
  DEPENDS outputs/generated.timestamp
)


# Initially create generated files, if they don't yet exist
if( NOT EXISTS ${CMAKE_BINARY_DIR}/outputs/generated.timestamp )
  message( "-- Running autogen" )
  execute_process(
    COMMAND ${CMAKE_COMMAND} -e mkdir -p ${CMAKE_BINARY_DIR}/outputs

    COMMAND
    python ${CMAKE_CURRENT_SOURCE_DIR}/autogen.py
    --input-dir ${CMAKE_CURRENT_SOURCE_DIR}/inputs
    --output-dir ${CMAKE_BINARY_DIR}/outputs
    --cmake ${CMAKE_BINARY_DIR}/outputs/generated_srcs.cmake

    COMMAND ${CMAKE_COMMAND} -E touch ${CMAKE_BINARY_DIR}/outputs/generated.timestamp
    )
endif()


set (SOURCES
  main.cpp
  )


# Include list of generated files to build the library
include( ${CMAKE_CURRENT_BINARY_DIR}/outputs/generated_srcs.cmake )

add_executable(cmk ${SOURCES} ${GENERATED_SRCS})
add_dependencies(cmk autogen)

target_include_directories(cmk PUBLIC ${CMAKE_CURRENT_BINARY_DIR}/outputs)

