from enum import Enum
import random
import pathlib


def random_part_type():
    score = random.randrange(0, 100)

    if 0 <= score < 40:
        return PartType.ANGLE
    elif 40 <= score < 80:
        return PartType.FLANGE
    elif 80 <= score < 90:
        return PartType.TEE
    elif 90 <= score < 100:
        return PartType.CROSS


class PartType(Enum):

    ANGLE = 1
    TEE = 2
    FLANGE = 3
    CROSS = 4

    def number_of_connections(self) -> int:
        if self == self.ANGLE:
            return 2
        elif self == self.TEE:
            return 3
        elif self == self.FLANGE:
            return 2
        elif self == self.CROSS:
            return 4

    def part_model_file(self) -> pathlib.Path:
        resource_dir = pathlib.Path(__file__).parent.parent.parent / "resources" / "3Dmodels"

        if self == self.ANGLE:
            return resource_dir / "coude.obj"
        elif self == self.TEE:
            return resource_dir / "te.obj"
        elif self == self.FLANGE:
            return resource_dir / "pipe4.obj"
        elif self == self.CROSS:
            return resource_dir / "cross.obj"
