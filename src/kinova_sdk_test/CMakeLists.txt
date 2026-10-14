cmake_minimum_required(VERSION 3.14)

project(kinova_sdk_test)

if(NOT CMAKE_CXX_STANDARD)
    set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    add_compile_options(-Wall -Wextra)
endif()

#####################################################
# EXACTAMENTE igual que el driver
#####################################################

add_definitions(-D_OS_UNIX=1)

#####################################################

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(kortex_api REQUIRED)

#####################################################
# Kortex Binary API
#####################################################

add_library(KortexApiCpp STATIC IMPORTED)

set_target_properties(KortexApiCpp PROPERTIES
    IMPORTED_LOCATION
    /home/alexander/kinova_ws/install/kortex_api/lib/libKortexApiCpp.a
)

target_link_libraries(KortexApiCpp
    INTERFACE pthread
)

#####################################################
# Test executable
#####################################################

add_executable(sdk_connection_test
    src/sdk_connection_test.cpp
)

ament_target_dependencies(
    sdk_connection_test
    rclcpp
    kortex_api
)

target_link_libraries(
    sdk_connection_test
    KortexApiCpp
)

install(
    TARGETS sdk_connection_test
    DESTINATION lib/${PROJECT_NAME}
)

ament_package()
