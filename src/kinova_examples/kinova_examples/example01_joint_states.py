#!/usr/bin/env python3

import math
import os
import time

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import JointState

from kinova_examples.utilities import rad2deg


class JointStateMonitor(Node):

    def __init__(self):
        super().__init__("example01_joint_states")

        self.subscription = self.create_subscription(
            JointState,
            "/joint_states",
            self.callback,
            10
        )

        self.last_time = time.time()
        self.counter = 0

    def callback(self, msg):

        self.counter += 1

        now = time.time()

        if now - self.last_time < 0.25:
            return

        frequency = self.counter / (now - self.last_time)

        self.counter = 0
        self.last_time = now

        os.system("clear")

        print("=" * 60)
        print("KINOVA GEN3 LITE")
        print("=" * 60)

        for name, position in zip(msg.name, msg.position):

            if "finger" in name:
                print(f"{name:30s}: {position:.4f}")
            else:
                print(f"{name:30s}: {rad2deg(position):8.2f} deg")

        print()

        print(f"Update rate : {frequency:.1f} Hz")
        print(f"Timestamp   : {msg.header.stamp.sec}.{msg.header.stamp.nanosec}")


def main():

    rclpy.init()

    node = JointStateMonitor()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()
