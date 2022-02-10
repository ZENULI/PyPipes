from networkx import Graph
from numpy import ndarray

from src.core.PartType import PartType


class PipelinePart:

    def __init__(self, part_type: PartType, coordinates: ndarray, direction: ndarray, radius: float) -> None:
        assert coordinates.shape == (3, 1)
        assert direction.shape == (3, 1)

        self._part_type = part_type
        self._coordinates = coordinates
        self._direction = direction
        self._radius = radius

    @property
    def part_type(self) -> PartType:
        return self._part_type

    @part_type.setter
    def part_type(self, value: PartType) -> None:
        self._part_type = PartType

    @property
    def coordinates(self) -> ndarray:
        return self._coordinates

    @coordinates.setter
    def coordinates(self, value: ndarray) -> None:
        assert value.shape == (3, 1)
        self._coordinates = value

    @property
    def direction(self) -> ndarray:
        return self._direction

    @direction.setter
    def direction(self, value: ndarray) -> None:
        assert value.shape == (3, 1)
        self._direction = value

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        self._radius = value


class PipelineGraph:

    def __init__(self) -> None:
        self._graph = Graph()

    def add_node(self, index: int, part: PipelinePart) -> None:
        self._graph.add_node((index, {"part": part}))

    def add_edge(self, start: int, end: int, weight: float) -> None:
        self._graph.add_edge(start, end, weight=weight)
