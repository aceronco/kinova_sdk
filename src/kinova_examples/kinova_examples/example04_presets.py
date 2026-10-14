
#!/usr/bin/env python3

import time

import rclpy

from kinova_examples.robot import KinovaRobot


def main():

    rclpy.init()

    robot = KinovaRobot()

    robot.wait_for_robot()

    print("ZERO")
    robot.zero()

    time.sleep(3)

    print("HOME")
    robot.home()

    time.sleep(5)

    print("SAFE")
    robot.safe()

    time.sleep(5)

    print("ZERO")
    robot.zero()
    
    time.sleep(3)

    print("SAFE")
    robot.safe()
    
    print("HOME")
    robot.home()

    robot.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()
