cmake_minimum_required(VERSION 3.10)
project(wrench_stress_test)

set(CMAKE_CXX_STANDARD 14)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/CMakeModules/")

find_package(SimGrid REQUIRED)

# wrench library and dependencies
find_library(WRENCH_LIBRARY NAMES wrench)
find_library(SimGrid_LIBRARY NAMES simgrid)

include_directories(src /usr/include /usr/local/include /opt/local/include ${SimGrid_INCLUDE_DIR})

add_executable(wrench_stress_test
        src/main.cpp
        src/Simulator.cpp
        src/Simulator.h
        src/StressTestWMS.cpp
        src/StressTestWMS.h
        CMakeLists.txt)

target_link_libraries(wrench_stress_test
        ${WRENCH_LIBRARY}
        ${SimGrid_LIBRARY}
	#	-lprofiler
        )



