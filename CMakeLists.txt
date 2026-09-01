cmake_minimum_required(VERSION 3.16)

project(rrevcan LANGUAGES C)

file(GLOB_RECURSE RREVCAN_SOURCES CONFIGURE_DEPENDS
    ${CMAKE_CURRENT_SOURCE_DIR}/src/*.c
)

add_library(rrevcan STATIC ${RREVCAN_SOURCES})

target_include_directories(rrevcan PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/src
)
