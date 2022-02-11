from enum import Enum
import random


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

    def number_of_connections(self):
        if self == self.ANGLE:
            return 2
        elif self == self.TEE:
            return 3
        elif self == self.FLANGE:
            return 2
        elif self == self.CROSS:
            return 4
