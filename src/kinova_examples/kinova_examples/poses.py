#para ejemplo06

import yaml  #para el 07

class PoseMixin:

    def save_current_pose(self, name):

        joints = self.get_joint_positions_deg()

        self.saved_poses[name] = joints[:6]

        self.get_logger().info(
            f"Pose '{name}' saved."
        )


    def go_to_pose(self, name):

        if name not in self.saved_poses:

            self.get_logger().error(
                f"Pose '{name}' does not exist."
            )

            return False

        return self.move_joints(
            self.saved_poses[name])

    def list_poses(self):

        return list(self.saved_poses.keys())        
    
    def delete_pose(self, name):

        if name in self.saved_poses:

            del self.saved_poses[name]    

    def save_poses_yaml(self, filename):

        with open(filename, "w") as file:

            yaml.dump(
                self.saved_poses,
                file,
                sort_keys=False
            )

        self.get_logger().info(
            f"Saved poses to {filename}"
        )            

    def load_poses_yaml(self, filename):

        with open(filename, "r") as file:

            self.saved_poses = yaml.safe_load(file)

        self.get_logger().info(
            f"Loaded poses from {filename}"
        )

    def print_poses(self):

        print()

        for name, joints in self.saved_poses.items():

            print(name)

            for i, value in enumerate(joints):

                print(
                    f"  Joint {i+1}: {value:8.2f}"
                )

            print()    