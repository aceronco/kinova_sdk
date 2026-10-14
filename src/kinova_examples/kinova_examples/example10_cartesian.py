#!/usr/bin/env python3

import rclpy

from kinova_examples.robot import KinovaRobot


def main():

    rclpy.init()

    robot = KinovaRobot()

    robot.wait_for_robot()

    print("Moving robot to Cartesian pose...")

    robot.move_cartesian(
        x=0.40,          #valido 0.4  rango  0.15 cerca a base a 0.4  al frente
        y=0.25,        #valido 0.10   rango  -0.25 derecha a 0.25 izq  
        z=0.10,          #valido 0.1   rango  0.05 abajo a  0.30
        theta_x=180,
        theta_y=0,
        theta_z=90,
        duration=4.0,
    )

    print("Motion completed.")

    robot.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()