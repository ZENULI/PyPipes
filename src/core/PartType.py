import json
from enum import Enum
import random
import pathlib
import numpy as np


class PartType(Enum):

    ANGLE = 1
    TEE = 2
    CROSS = 3

    PIPE_1 = 4
    PIPE_2 = 5
    PIPE_3 = 6
    PIPE_4 = 7

    def distance_per_axis(self) -> dict:
        if self == self.ANGLE:
            return {'x': 1.21041, 'y': 0.5, 'z': 1.21041}
        elif self == self.TEE:
            return {'x': 1.286665, 'y': 0.5, 'z': 1.286665}
        elif self == self.CROSS:
            return {'x': 1.06615, 'y': 0.5, 'z': 1.286665}
        elif self == self.PIPE_1:
            return {'x': 0.5, 'y': 0.5, 'z': 1.784005}
        elif self == self.PIPE_2:
            return {'x': 0.5, 'y': 0.5, 'z': 2.97334}
        elif self == self.PIPE_3:
            return {'x': 0.5, 'y': 0.5, 'z': 5.6493}
        elif self == self.PIPE_4:
            return {'x': 0.5, 'y': 0.5, 'z': 2.97334}

    def connections_per_axis(self) -> list:
        if self == self.ANGLE:
            return ["x", "-z"]
        elif self == self.TEE:
            return ["-x", "z", "-z"]
        elif self == self.CROSS:
            return ["x", "-x", "z", "-z"]
        else:
            return ["z", "-z"]

    def part_model_file(self) -> pathlib.Path:
        resource_dir = pathlib.Path(__file__).parent.parent.parent / "resources" / "3Dmodels"

        if self == self.ANGLE:
            return resource_dir / "coude.ply"
        elif self == self.TEE:
            return resource_dir / "te.ply"
        elif self == self.CROSS:
            return resource_dir / "cross.ply"
        elif self == self.PIPE_1:
            return resource_dir / "pipe1.ply"
        elif self == self.PIPE_2:
            return resource_dir / "pipe2.ply"
        elif self == self.PIPE_3:
            return resource_dir / "pipe3.ply"
        elif self == self.PIPE_4:
            return resource_dir / "pipe4.ply"


class EnumEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, PartType):
            return {"__enum__": str(o)}
        if (isinstance(o, np.int32) or isinstance(o, np.int64)):
            return int(o)
        return json.JSONEncoder.default(self, o)


def as_part_type(d):
    if "__enum__" in d:
        name, member = d["__enum__"].split(".")
        return getattr(PartType, member)
    else:
        return d


def random_part_type() -> PartType:
    score = random.randrange(0, 100)

    if 0 <= score < 40:
        return PartType.ANGLE
    elif 40 <= score < 80:
        return PartType.TEE
    elif 80 <= score < 100:
        return PartType.CROSS


def random_pipe_type() -> PartType:
    score = random.randrange(0, 100)

    if 0 <= score < 25:
        return PartType.PIPE_1
    elif 25 <= score < 50:
        return PartType.PIPE_2
    elif 50 <= score < 75:
        return PartType.PIPE_3
    elif 75 <= score < 100:
        return PartType.PIPE_4
