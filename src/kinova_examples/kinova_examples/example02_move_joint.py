#!/usr/bin/env python3
# EJEMPLO mover articulaciones y dejar el brazo vertical
import math

import rclpy

from kinova_examples.robot import KinovaRobot


def main():

    rclpy.init()

    robot = KinovaRobot()

    robot.wait_for_robot()

    print(robot.get_joint_positions_deg())

    robot.print_joint_positions()

    robot.move_joint(0, 0)

    robot.move_joint(1, 0)

    robot.move_joint(2, 0)

    robot.move_joint(3, 0)

    robot.move_joint(4, 0)

    robot.move_joint(5, 0)    

    robot.destroy_node()

    rclpy.shutdown()

if __name__ == "__main__":
    main()
