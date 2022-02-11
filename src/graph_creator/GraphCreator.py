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

        rx = random.randrange(0, 90, 15)
        ry = random.randrange(0, 90, 15)
        rz = random.randrange(0, 90, 15)
        direction = np.asarray([rx, ry, rz])

        radius = random.uniform(min_radius, max_radius)

        part_type = random_part_type()

        part = PipelinePart(part_type, coordinate, direction, radius)

        all_parts = [part]

        current_parts = 0
        while current_parts < nb_parts:
            last_coordinate = coordinate

            part_type = random_part_type()

            rx = random.randrange(0, 90, 15)
            ry = random.randrange(0, 90, 15)
            rz = random.randrange(0, 90, 15)
            direction = np.asarray([rx, ry, rz])

            dx = random.uniform(max_radius * 2, max_radius * 10)
            dy = random.uniform(max_radius * 2, max_radius * 10)
            dz = random.uniform(max_radius * 2, max_radius * 10)

            coordinate = np.asarray([last_coordinate[0] + dx, last_coordinate[1] + dy, last_coordinate[2] + dz])

            radius = random.uniform(min_radius, max_radius)

            part = PipelinePart(part_type, coordinate, direction, radius)
            all_parts.append(part)

            current_parts += 1

        for i in range(0, len(all_parts)):
            graph.add_node(i, all_parts[i])

        graph.complete()
        graph.visualize()

        return graph

    def build_graph(self, point_cloud: PointCloud) -> PipelineGraph:
        assert point_cloud.is_classified()

        raise NotImplementedError("Not yet implemented")
