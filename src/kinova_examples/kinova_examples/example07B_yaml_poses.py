#!/usr/bin/env python3

import time

import rclpy

from kinova_examples.robot import KinovaRobot


def main():

    rclpy.init()

    robot = KinovaRobot()

    robot.wait_for_robot()

    robot.home()

    robot.load_poses_yaml("poses.yaml")

    robot.go_to_pose("left")

    time.sleep(3)

    robot.go_to_pose("right")

    time.sleep(3)

    robot.go_to_pose("home")

    robot.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":

    main()