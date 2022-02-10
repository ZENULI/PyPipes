from src.graph_creator.core.PipelineGraph import PipelineGraph, PipelinePart
from src.core.PointCloud import PointCloud

from src.core.PartType import random_part_type

import random
import numpy as np


class GraphCreator:

    def __init__(self):
        pass

    def create_random_graph(self, nb_parts: int, min_radius: float = 1.0, max_radius: float = 5.0) -> PipelineGraph:
        graph = PipelineGraph()

        # Create first part
        coordinate = np.asarray([0., 0., 0.])
        direction = np.asarray([0., 0., 0.])

        radius = random.uniform(min_radius, max_radius)

        part_type = random_part_type()

        part = PipelinePart(part_type, coordinate, direction, radius)
        graph.add_node(0, part)

        current_parts = 1
        while current_parts < nb_parts:
            missing_connections = part_type.number_of_connections() - 1

            last_part = current_parts - 1
            last_coordinate = coordinate

            for i in range(0, missing_connections):
                part_type = random_part_type()

                dx = random.randrange(0, 90, 15)
                dy = random.randrange(0, 90, 15)
                dz = random.randrange(0, 90, 15)

                coordinate = np.asarray([last_coordinate[0] + dx, last_coordinate[1] + dy, last_coordinate[2] + dz])
                direction = np.zeros((1, 3))

                radius = random.uniform(min_radius, max_radius)

                part = PipelinePart(part_type, coordinate, direction, radius)
                distance = random.uniform(max_radius * 2, max_radius * 10)

                graph.add_node(current_parts, part)
                graph.add_edge(last_part, current_parts, distance)

                current_parts += 1

        graph.visualize()

        return graph

    def build_graph(self, point_cloud: PointCloud) -> PipelineGraph:
        assert point_cloud.is_classified()

        raise NotImplementedError("Not yet implemented")
