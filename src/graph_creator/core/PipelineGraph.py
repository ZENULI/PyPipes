import networkx as nx
import numpy as np
import random
from networkx import Graph
from numpy import ndarray

from src.core.PartType import PartType


class PipelinePart:

    def __init__(self, part_type: PartType, coordinates: ndarray, direction: ndarray, radius: float) -> None:
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
        self._coordinates = value

    @property
    def direction(self) -> ndarray:
        return self._direction

    @direction.setter
    def direction(self, value: ndarray) -> None:
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

    def add_node(self, index: int, p: PipelinePart) -> None:
        self._graph.add_node(index, type=p.part_type, coordinates=p.coordinates, direction=p.direction, radius=p.radius)

    def add_edge(self, start: int, end: int, weight: float) -> None:
        self._graph.add_edge(start, end, weight=weight)

    def complete(self) -> None:
        nb_nodes = self._graph.number_of_nodes()

        def neighbours(node):
            return self._graph.degree[node]

        def expected_neighbours(node):
            return self._graph.nodes[node]['type'].number_of_connections()

        for i in range(0, nb_nodes):
            start_coordinates = self._graph.nodes[i]['coordinates']

            candidates = [c for c in range(0, nb_nodes) if c != i]
            random.shuffle(candidates)

            neigh = neighbours(i)
            expected = expected_neighbours(i)

            while neigh < expected:
                connection = None
                for candidate in candidates:
                    if neighbours(candidate) < expected_neighbours(candidate):
                        connection = candidate
                        break

                if connection:
                    end_coordinates = self._graph.nodes[connection]['coordinates']
                    distance = np.linalg.norm(start_coordinates - end_coordinates)

                    self._graph.add_edge(i, connection, weight=distance)

                neigh += 1

    def visualize(self) -> None:
        nx.draw(self._graph)

    def clear(self) -> None:
        self._graph.clear()
