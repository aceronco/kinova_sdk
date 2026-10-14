from dataclasses import dataclass


@dataclass
class JointConfiguration:

    j1: float = 0.0
    j2: float = 0.0
    j3: float = 0.0
    j4: float = 0.0
    j5: float = 0.0
    j6: float = 0.0

    def to_list(self):

        return [
            self.j1,
            self.j2,
            self.j3,
            self.j4,
            self.j5,
            self.j6,
        ]
