#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node
from .motion import MotionMixin  # se agrego luego de crear archivo motion
from .gripper import GripperMixin  #primero hacer gripper.py
from .poses import PoseMixin
from .sequence import SequenceMixin #ejemplo 8

from sensor_msgs.msg import JointState

from rclpy.action import ActionClient
from control_msgs.action import FollowJointTrajectory

from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint


from .kinematics import KinematicsMixin


from .state import StateMixin


class KinovaRobot(Node,
        StateMixin,
        MotionMixin,
        GripperMixin,
        PoseMixin,
        SequenceMixin,KinematicsMixin):  #se agrega cada herencia luego de crear cada modulo y clase

    def __init__(self):

        super().__init__("kinova_robot")

        self.joint_state = None

        self.subscription = self.create_subscription(
            JointState,
            "/joint_states",
            self.joint_state_callback,
            10)

        self.action_client = ActionClient(
            self,
            FollowJointTrajectory,
            "/joint_trajectory_controller/follow_joint_trajectory"
        )

        self.saved_poses = {} #para ejemplo 6

    def _send_joint_goal(self, joint_positions_deg, duration=3.0):
        if len(joint_positions_deg) != 6:
            raise ValueError("Expected 6 joint values")

        goal_msg = FollowJointTrajectory.Goal()

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

        point.positions = [
            math.radians(v)
            for v in joint_positions_deg
        ]

        point.time_from_start.sec = int(duration)
        point.time_from_start.nanosec = int(
            (duration-int(duration))*1e9
        )

        traj.points.append(point)

        goal_msg.trajectory = traj

        self._action_client.wait_for_server()

        future = self._action_client.send_goal_async(goal_msg)

        rclpy.spin_until_future_complete(self, future)

        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().error("Goal rejected")
            return False

        result_future = goal_handle.get_result_async()

        rclpy.spin_until_future_complete(self, result_future)

        return True

    def joint_state_callback(self,msg):

        self.joint_state = msg

    def wait_for_robot(self):

        self.get_logger().info("Waiting for joint states...")

        while rclpy.ok() and self.joint_state is None:
            rclpy.spin_once(self,timeout_sec=0.1)

        self.get_logger().info("Robot connected.")

        self.get_logger().info("Waiting trajectory server...")

        self.action_client.wait_for_server()

        self.get_logger().info("Trajectory server ready.")

        self.initialize_gripper()

        self.get_logger().info("Robot ready.")


    def get_joint_positions(self):

        rclpy.spin_once(self, timeout_sec=0.1)

        return list(self.joint_state.position)
    

    def get_joint_positions_deg(self):

        joints = self.get_joint_positions()

        return [
            math.degrees(q)
            for q in joints[:6]
        ]
    
    def get_all_joint_positions_deg(self):

        joints = self.get_joint_positions()

        return [
            math.degrees(q)
            for q in joints
        ]
    
    def print_joint_positions(self):

        joints=self.get_joint_positions()

        print()

        for i,value in enumerate(joints):

            print(f"Joint {i+1}: {math.degrees(value):8.2f} deg")
    

