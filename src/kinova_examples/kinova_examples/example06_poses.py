
#!/usr/bin/env python3

import time

import rclpy

from kinova_examples.robot import KinovaRobot


def main():

    rclpy.init()

    robot = KinovaRobot()

    robot.wait_for_robot()

    robot.home()

    robot.save_current_pose("home")

    robot.offset_joint(0,20)

    robot.save_current_pose("left")

    robot.offset_joint(0,-40)

    robot.save_current_pose("right")

    print(robot.list_poses())

    robot.go_to_pose("left")

    time.sleep(3)

    robot.go_to_pose("right")

    time.sleep(3)

    robot.go_to_pose("home")
    
    robot.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()