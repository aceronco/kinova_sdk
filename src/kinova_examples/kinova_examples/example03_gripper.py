#!/usr/bin/env python3

import time

import rclpy

from kinova_examples.robot import KinovaRobot


def main():

    rclpy.init()

    robot = KinovaRobot()

    robot.wait_for_robot()

    time.sleep(3)
    robot.open_gripper()

    time.sleep(1)
   
    robot.close_gripper()

    time.sleep(1)

#    robot.set_gripper(0)  #porcentaje0  abierto #100 cerrado para 1 cm

    time.sleep(2)
#    robot.move_gripper_raw(0.015) #abierto
  #  robot.move_gripper_raw(0.7) #cerrado a 1 cm
  #  time.sleep(2)
  

    robot.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()
