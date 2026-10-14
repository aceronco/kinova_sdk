cmake_minimum_required(VERSION 3.8)
project(kinova_kinematics_cpp)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

##############################################
# Dependencies
##############################################

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)

find_package(rosidl_default_generators REQUIRED)

find_package(kortex_api REQUIRED)

##############################################
# Services
##############################################

rosidl_generate_interfaces(${PROJECT_NAME}
    "srv/ComputeIK.srv"
    DEPENDENCIES geometry_msgs
)

ament_export_dependencies(rosidl_default_runtime)

##############################################
# Kortex API
##############################################

add_library(KortexApiCpp STATIC IMPORTED)

set_target_properties(KortexApiCpp PROPERTIES
    IMPORTED_LOCATION
    /home/alexander/kinova_ws/install/kortex_api/lib/libKortexApiCpp.a
)

target_link_libraries(KortexApiCpp
    INTERFACE pthread
)

##############################################
# Library
##############################################

add_library(kinova_kinematics

    src/kinova_kinematics.cpp
)

target_include_directories(kinova_kinematics
PUBLIC
    include

    /home/alexander/kinova_ws/install/kortex_api/include/kortex_api
)

ament_target_dependencies(kinova_kinematics

    rclcpp
)

target_link_libraries(kinova_kinematics

    KortexApiCpp
)

##############################################

install(
    TARGETS kinova_kinematics
    DESTINATION lib
)

install(
    DIRECTORY include/
    DESTINATION include
)

##############################################

if(BUILD_TESTING)

find_package(ament_lint_auto REQUIRED)

set(ament_cmake_cpplint_FOUND TRUE)
set(ament_cmake_copyright_FOUND TRUE)

ament_lint_auto_find_test_dependencies()

endif()


#agregado se inserta desde aca 
add_executable(sdk_connection_test
    src/sdk_connection_test.cpp
)

target_compile_definitions(sdk_connection_test PRIVATE _OS_UNIX) #agregado
target_include_directories(sdk_connection_test
PUBLIC
    include
    /home/alexander/kinova_ws/install/kortex_api/include/kortex_api
)

ament_target_dependencies(sdk_connection_test
    rclcpp
)

target_link_libraries(sdk_connection_test
    KortexApiCpp
)

install(
    TARGETS sdk_connection_test
    DESTINATION lib/${PROJECT_NAME}
)
#hasta aca

ament_package()
