from src.core.PartType import PartType

from numpy import ndarray


class Point:

    def __init__(self, x: float, y: float, z: float) -> None:
        self._x = x
        self._y = y
        self._z = z

        self._center = None
        self._part_type = None
        self._radius = None
        self._direction = None

    def clear_labels(self) -> None:
        self._center = None
        self._part_type = None
        self._radius = None
        self._direction = None

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def z(self) -> float:
        return self._z

    @property
    def center(self) -> ndarray:
        return self._center

    @center.setter
    def center(self, value: ndarray) -> None:
        self._center = value

    @property
    def part_type(self) -> PartType:
        return self._part_type

    @part_type.setter
    def part_type(self, value: PartType) -> None:
        self._part_type = value

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        self._radius = value

    @property
    def direction(self) -> ndarray:
        return self._direction

    @direction.setter
    def direction(self, value: ndarray) -> None:
        self._direction = value

    def is_classified(self) -> bool:
        return self._center is not None and self._part_type is not None and self._radius is not None and \
               self._direction is not None
