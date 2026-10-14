
#!/usr/bin/env python3

import time

import rclpy

from kinova_examples.robot import KinovaRobot


def main():

    rclpy.init()

    robot = KinovaRobot()

    robot.wait_for_robot()

    robot.home()

    robot.offset_joint(0, 10)

    robot.offset_joint(0, -10)

    robot.offset_joint(1, 5)

    robot.offset_joint(1, -5)

    robot.home()

    robot.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()