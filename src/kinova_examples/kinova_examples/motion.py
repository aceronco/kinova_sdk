#!/usr/bin/env python3

import math

import rclpy


PRESET_POSES = {
    "home": [0, -90, 90, 0, -90, -90],
    "safe": [0, -70, 90, 0, -90, 0],
    "zero": [0, 0, 0, 0, 0, 0],
}

from builtin_interfaces.msg import Duration

from control_msgs.action import FollowJointTrajectory

from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint



class MotionMixin:

    def move_joints(self, joints_deg, duration=3.0):
        """
        Mueve todas las articulaciones.

        joints_deg : lista de 6 ángulos en grados.
        """

        if len(joints_deg) != 6:
            raise ValueError("Expected 6 joint values")

        goal = FollowJointTrajectory.Goal()

        traj = JointTrajectory()

        traj.joint_names = [
            "joint_1",
            "joint_2",
            "joint_3",
            "joint_4",
            "joint_5",
            "joint_6",
        ]

        point = JointTrajectoryPoint()

        # El controlador espera radianes
        point.positions = [
            math.radians(q)
            for q in joints_deg
        ]

        point.time_from_start = Duration(
            sec=int(duration),
            nanosec=int((duration % 1.0) * 1e9)
        )

        traj.points.append(point)

        goal.trajectory = traj

        self.get_logger().info("Waiting trajectory server...")

        self.action_client.wait_for_server()

        self.get_logger().info("Sending trajectory...")

        future = self.action_client.send_goal_async(goal)

        rclpy.spin_until_future_complete(self, future)

        goal_handle = future.result()

        if goal_handle is None:

            self.get_logger().error("Goal failed.")

            return False

        if not goal_handle.accepted:

            self.get_logger().error("Goal rejected.")

            return False

        self.get_logger().info("Trajectory accepted.")

        result_future = goal_handle.get_result_async()

        rclpy.spin_until_future_complete(
            self,
            result_future
        )

        result = result_future.result().result

        if result.error_code == 0:

            self.get_logger().info("Trajectory completed.")

            return True

        self.get_logger().error(
            f"Trajectory failed. Error={result.error_code}"
        )

        return False

    def move_joint(self, joint_index, angle_deg):
        """
        Cambia únicamente una articulación.
        """

        joints = self.get_joint_positions_deg()

        joints = joints[:6]      # <-- importante

        joints[joint_index] = angle_deg

        return self.move_joints(joints)

    def offset_joint(self, joint_index, delta_deg):

        joints = self.get_joint_positions_deg()

        joints = joints[:6]

        joints[joint_index] += delta_deg

        return self.move_joints(joints)
    
    def offset_joints(self, delta):

        joints = self.get_joint_positions_deg()

        joints = joints[:6]

        for i in range(6):
            joints[i] += delta[i]

        return self.move_joints(joints)
    
    def home(self):
        return self.move_joints(PRESET_POSES["home"])


    def zero(self):

        return self.move_joints(PRESET_POSES["zero"])


    def safe(self):

        return self.move_joints(PRESET_POSES["safe"])

    
