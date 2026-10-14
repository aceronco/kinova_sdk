#!/usr/bin/env python3

import rclpy

from rclpy.action import ActionClient

from control_msgs.action import GripperCommand




class GripperMixin:

    GRIPPER_OPEN = 0.020
    GRIPPER_CLOSED = 0.7

    def initialize_gripper(self):

        self.gripper_client = ActionClient(
            self,
            GripperCommand,
            "/gen3_lite_2f_gripper_controller/gripper_cmd"
        )

        self.get_logger().info("Waiting gripper server...")

        self.gripper_client.wait_for_server()

        self.get_logger().info("Gripper server ready.")

    def move_gripper_raw(self, position, max_effort=20.0):

        goal = GripperCommand.Goal()

        goal.command.position = position
        goal.command.max_effort = max_effort

        self.get_logger().info("Waiting gripper server...")

        self.gripper_client.wait_for_server()

        self.get_logger().info("Sending gripper command...")

        future = self.gripper_client.send_goal_async(goal)

        rclpy.spin_until_future_complete(self, future)

        goal_handle = future.result()

        if goal_handle is None or not goal_handle.accepted:

            self.get_logger().error("Gripper goal rejected.")

            return False

        result_future = goal_handle.get_result_async()

        rclpy.spin_until_future_complete(self, result_future)

        result = result_future.result().result

        if result.reached_goal:

            self.get_logger().info("Gripper movement completed.")

            return True

        self.get_logger().warning("Gripper did not reach target.")

        return False



    def move_gripper(self, position, max_effort=20.0):

        """
        position:
            0.0 -> completamente abierto
            1.0 -> completamente cerrado
        """

        goal = GripperCommand.Goal()

        goal.command.position = float(position)

        goal.command.max_effort = float(max_effort)

        self.get_logger().info(
            f"Moving gripper to {position:.2f}"
        )

        future = self.gripper_client.send_goal_async(goal)

        rclpy.spin_until_future_complete(self, future)

        goal_handle = future.result()

        if goal_handle is None:

            self.get_logger().error("No response from gripper.")

            return False

        if not goal_handle.accepted:

            self.get_logger().error("Gripper goal rejected")

            return False

        result_future = goal_handle.get_result_async()

        rclpy.spin_until_future_complete(
            self,
            result_future
        )

        self.get_logger().info("Gripper motion finished.")

        return True

    def open_gripper(self):

        return self.move_gripper(0.04)

    def close_gripper(self):

        return self.move_gripper(0.5)
    


    def set_gripper(self, percent):

        percent = max(0.0, min(100.0, percent))

        position = (
            self.GRIPPER_OPEN
            + (percent / 100.0)
            * (self.GRIPPER_CLOSED - self.GRIPPER_OPEN)
        )

        return self.move_gripper_raw(position)

    def get_gripper_position(self):

        joints = self.get_joint_positions()

        return joints[6]

    def get_gripper_percent(self):

        position = self.get_gripper_position()

        percent = (
            (self.GRIPPER_OPEN - position)
            / (self.GRIPPER_OPEN - self.GRIPPER_CLOSED)
        ) * 100.0

        return max(0.0, min(100.0, percent))