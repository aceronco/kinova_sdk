import time


class SequenceMixin:

    def run_sequence(self, sequence, wait=0.0):

        self.get_logger().info(
            f"Executing sequence ({len(sequence)} poses)"
        )

        for pose in sequence:

            self.get_logger().info(
                f"Moving to '{pose}'"
            )

            ok = self.go_to_pose(pose)

            if not ok:

                self.get_logger().error(
                    f"Pose '{pose}' failed."
                )

                return False

            if wait > 0:

                time.sleep(wait)

        self.get_logger().info(
            "Sequence completed."
        )

        return True