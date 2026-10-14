#!/usr/bin/env python3

import rclpy

from kinova_examples.robot import KinovaRobot


def main():

    rclpy.init()

    robot = KinovaRobot()

    robot.wait_for_robot()

    robot.load_poses_yaml("poses.yaml")

    robot.print_poses()

    sequence = [

        "home",

        "left",

        "right",

        "home"

    ]

    robot.run_sequence(sequence, wait=2.0)

    robot.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":

    main()