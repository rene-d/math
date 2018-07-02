#

cmake_minimum_required(VERSION 3.5)

project(projecteuler)

set(CMAKE_EXPORT_COMPILE_COMMANDS on)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_C_STANDARD 11)

set(CMAKE_CXX_FLAGS "-Wall -Wextra -Wconversion -Wsign-conversion")
set(CMAKE_C_FLAGS "-Wall -Wextra -Wconversion -Wsign-conversion")

#set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3")

add_executable(p040 p040.c)
add_executable(p041 p041.cpp)
add_executable(p043 p043.cpp)
add_executable(p044 p044.cpp)
add_executable(p045 p045.cpp)
add_executable(p051 p051.c)
add_executable(p062 p062.cpp)
add_executable(p070 p070.c)
add_executable(p074 p074.cpp)
add_executable(p081 p081.cpp)
add_executable(p082 p082.cpp)
add_executable(p083 p083.cpp)
add_executable(p085 p085.c)
add_executable(p091 p091.c)
add_executable(p092 p092.c)
add_executable(p095 p095.cpp)
add_executable(p097 p097.c)
add_executable(p206 p206.c)
add_executable(p345 p345.cpp)

#set_source_files_properties(p085.c PROPERTIES LANGUAGE CXX)

target_link_libraries(p085 m)
target_link_libraries(p206 m)
