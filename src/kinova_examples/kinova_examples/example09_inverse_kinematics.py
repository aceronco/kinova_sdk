#!/usr/bin/env python3

"""
Example 9
Compute inverse kinematics using the official Kinova SDK.
"""

import rclpy

from kinova_examples.robot import KinovaRobot


def main():

    rclpy.init()

    robot = KinovaRobot()

    try:

        robot.wait_for_robot()

        print("Target pose")
        print(" x = 0.40")
        print(" y = 0.10")
        print(" z = 0.20")
        print(" rx = 180")
        print(" ry = 0")
        print(" rz = 90")

        q = robot.compute_ik(
            x=0.40,
            y=0.10,
            z=0.20,
            theta_x=180,
            theta_y=0,
            theta_z=90,
        )

        if q is None:

            print("No inverse kinematics solution found")

        else:

            print("\nInverse kinematics solution\n")

            for i, angle in enumerate(q, start=1):
                print(f"Joint {i}: {angle:.3f} deg")

    except Exception as e:

        print(e)

    finally:

        robot.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
