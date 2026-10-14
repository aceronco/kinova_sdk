cmake_minimum_required(VERSION 3.14)

project(kinova_sdk_bridge)

#
# C++
#
if(NOT CMAKE_CXX_STANDARD)
    set(CMAKE_CXX_STANDARD 14)
endif()

#
# Linux
#
add_definitions(-D_OS_UNIX=1)

########################################################
# Dependencies
########################################################

find_package(ament_cmake REQUIRED)

find_package(rclcpp REQUIRED)

find_package(geometry_msgs REQUIRED)

find_package(rosidl_default_generators REQUIRED)

find_package(kortex_api REQUIRED)

########################################################
# Service
########################################################

rosidl_generate_interfaces(${PROJECT_NAME}

    "srv/ComputeIK.srv"

    DEPENDENCIES
        geometry_msgs
)

########################################################
# Kinova SDK
########################################################

include(FetchContent)

FetchContent_Declare(
    kinova_binary_api
    URL https://artifactory.kinovaapps.com:443/artifactory/generic-public/kortex/API/2.5.0/linux_x86-64_x86_gcc.zip
    URL_HASH MD5=64bd86e7ab8bda90ef1fc7d6a356e080
)

FetchContent_MakeAvailable(kinova_binary_api)

add_library(KortexApiCpp STATIC IMPORTED)

set_target_properties(
    KortexApiCpp
    PROPERTIES

    IMPORTED_LOCATION
    ${kinova_binary_api_SOURCE_DIR}/lib/release/libKortexApiCpp.a

    INTERFACE_LINK_LIBRARIES
    pthread
)

add_dependencies(
    KortexApiCpp
    kortex_api
)

########################################################
# Executable
########################################################

add_executable(

    ik_service_node

    src/ik_service_node.cpp
)

target_include_directories(

    ik_service_node

    PRIVATE

    include
)

ament_target_dependencies(

    ik_service_node

    rclcpp
    geometry_msgs
    kortex_api
)

target_link_libraries(

    ik_service_node

    KortexApiCpp
)

rosidl_target_interfaces(

    ik_service_node

    ${PROJECT_NAME}

    "rosidl_typesupport_cpp"
)

########################################################
# Install
########################################################

install(

    TARGETS

        ik_service_node

    DESTINATION

        lib/${PROJECT_NAME}
)

install(

    DIRECTORY launch

    DESTINATION

        share/${PROJECT_NAME}
)

########################################################

ament_package()
