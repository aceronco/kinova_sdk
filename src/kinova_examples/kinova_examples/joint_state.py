from dataclasses import dataclass


@dataclass
class JointStateData:

    j1: float
    j2: float
    j3: float
    j4: float
    j5: float
    j6: float

    v1: float
    v2: float
    v3: float
    v4: float
    v5: float
    v6: float

    e1: float
    e2: float
    e3: float
    e4: float
    e5: float
    e6: float
