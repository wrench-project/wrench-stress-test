cmake_minimum_required(VERSION 3.14)
project(wrench_stress_test)

set(CMAKE_CXX_STANDARD 14)

include_directories(src /usr/include /usr/local/include /opt/local/include)

# wrench library and dependencies
find_library(WRENCH_LIBRARY NAMES wrench)
find_library(SIMGRID_LIBRARY NAMES simgrid)
find_library(PUGIXML_LIBRARY NAMES pugixml)

add_executable(wrench_stress_test
        src/main.cpp
        src/Simulator.cpp
        src/Simulator.h
        src/StressTestWMS.cpp
        src/StressTestWMS.h
        CMakeLists.txt)

target_link_libraries(wrench_stress_test
        ${WRENCH_LIBRARY}
        ${SIMGRID_LIBRARY}
        ${PUGIXML_LIBRARY}
        )



