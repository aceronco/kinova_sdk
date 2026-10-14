import math

import rclpy

class StateMixin:

    def get_joint_positions(self):

        rclpy.spin_once(self, timeout_sec=0.1)

        return list(self.joint_state.position)


    def get_joint_positions_deg(self):

        joints = self.get_joint_positions()

        return [math.degrees(q) for q in joints]


    def print_joint_positions(self):

        joints = self.get_joint_positions_deg()

        print()

        for i, value in enumerate(joints):

            print(f"Joint {i+1}: {value:8.2f} deg")
