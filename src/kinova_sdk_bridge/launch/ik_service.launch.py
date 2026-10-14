from launch import LaunchDescription

from launch_ros.actions import Node


def generate_launch_description():

    return LaunchDescription([

        Node(

            package="kinova_sdk_bridge",

            executable="ik_service_node",

            output="screen",

            parameters=[

                {
                    "robot_ip": "192.168.1.10",
                    "username": "estudiantes",
                    "password": "KINOVA-UMNG",
                }

            ],
        )

    ])
