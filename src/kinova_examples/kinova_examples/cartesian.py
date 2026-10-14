#!/usr/bin/env python3


class CartesianMixin:

    def get_pose(self):

        raise NotImplementedError(
            "Cartesian interface not implemented yet."
        )

    def move_cartesian(
        self,
        x,
        y,
        z,
        roll,
        pitch,
        yaw
    ):

        raise NotImplementedError(
            "Cartesian controller not implemented yet."
        )
    

    