#!/usr/bin/env python3

import os
import rclpy

from geometry_msgs.msg import Pose
from kinova_sdk_bridge.srv import ComputeIK


class KinematicsMixin:

    def compute_ik(
        self,
        x,
        y,
        z,
        theta_x,
        theta_y,
        theta_z,
    ):
        """
        Compute inverse kinematics using the Kinova C++ SDK.

        Parameters
        ----------
        x,y,z : float
            Position in meters.

        theta_x, theta_y, theta_z : float
            Orientation in degrees.

        Returns
        -------
        list[float]
            Joint angles in degrees.
        """
        client = self.create_client(ComputeIK, "compute_inverse_kinematics",)

        if not client.wait_for_service(timeout_sec=5.0):
            raise RuntimeError(
                "compute_inverse_kinematics service not available"
            )
        request = ComputeIK.Request()

        request.pose = Pose()

        request.pose.position.x = x
        request.pose.position.y = y
        request.pose.position.z = z

        request.pose.orientation.x = float(theta_x)
        request.pose.orientation.y = float(theta_y)
        request.pose.orientation.z = float(theta_z)
        request.pose.orientation.w = 1.0
    

        guess = self.get_joint_positions_deg()

        print("\nCurrent joint guess")

        for i, q in enumerate(guess):
            print(f"Joint {i+1}: {q:.3f}")

        request.guess = guess

        print(type(request.pose.position.x))
        print(type(request.pose.orientation.x))
        print(type(request.pose.orientation.y))
        print(type(request.pose.orientation.z))
        print(type(request.pose.orientation.w))

        print(request.pose)

        future = client.call_async(request)

        rclpy.spin_until_future_complete(
            self,
            future,
        )
        response = future.result()

        if response is None:
            raise RuntimeError("Service call failed")

        if not response.success:
            raise RuntimeError(response.message)

        return [
            response.joint1,
            response.joint2,
            response.joint3,
            response.joint4,
            response.joint5,
            response.joint6,
        ]



    def move_cartesian(
        self,
        x,
        y,
        z,
        theta_x,
        theta_y,
        theta_z,
        duration=3.0,
         ):
        """
        Computes inverse kinematics and executes the motion.
        """

        joints = self.compute_ik(
            x=x,
            y=y,
            z=z,
            theta_x=theta_x,
            theta_y=theta_y,
            theta_z=theta_z,
        )

        self.get_logger().info(
            "Executing Cartesian motion..."
        )

        return self.move_joints(
            joints,
            duration=duration,
        )


    def is_reachable(
        self,
        x,
        y,
        z,
        theta_x,
        theta_y,
        theta_z,
    ):
        """
        Returns True if the pose has an IK solution.
        """

        try:

            self.compute_ik(
                x,
                y,
                z,
                theta_x,
                theta_y,
                theta_z,
            )

            return True

        except Exception:

            return False
