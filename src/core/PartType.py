from enum import Enum
import random


def random_part_type():
    score = random.randrange(0, 50)

    if 0 <= score < 40:
        return PartType.ANGLE
    elif 40 <= score < 50:
        return PartType.TEE


class PartType(Enum):

    ANGLE = 1
    TEE = 2

    def number_of_connections(self):
        if self == self.ANGLE:
            return 2
        elif self == self.TEE:
            return 3
