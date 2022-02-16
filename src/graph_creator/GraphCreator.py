from src.graph_creator.core.PipelineGraph import PipelineGraph, PipelinePart
from src.core.PointCloud import PointCloud

from src.core.PartType import random_part_type, random_pipe_type

import numpy as np


class GraphCreator:

    def __init__(self):
        pass

    def create_random_graph(self, nb_parts: int) -> PipelineGraph:
        graph = PipelineGraph()

        # Create first part
        coordinate = np.asarray([0., 0., 0.])
        direction = np.asarray([0, 0, 0])
        radius = 1

        part_type = random_part_type()

        part_index = 0
        nb_pipes = 0

        part = PipelinePart(part_type, coordinate, direction, radius)

        graph.add_node(part_index, part)

        last_coordinate = coordinate
        last_part_type = part_type
        connections = last_part_type.connections_per_axis()

        end_parts = []

        for connection in connections:
            pipe, new_part = self.create_part_and_pipe_for_connection(connection, last_coordinate, last_part_type)

            part_index += 1
            graph.add_node(part_index, pipe)
            graph.add_edge(part_index - 1, part_index)
            nb_pipes += 1

            if part_index - nb_pipes >= nb_parts:
                return graph

            part_index += 1
            graph.add_node(part_index, new_part)
            graph.add_edge(part_index - 1, part_index)

            end_parts.append((new_part, connection))

        while len(end_parts) != 0:
            last_part_tuple = end_parts.pop(0)

            next_part = last_part_tuple[0]
            last_connection = last_part_tuple[1]

            occupied_connection = ""
            if last_connection == "x":
                occupied_connection = "-x"
            elif last_connection == "-x":
                occupied_connection = "x"
            elif last_connection == "y":
                occupied_connection = "-y"
            elif last_connection == "-y":
                occupied_connection = "y"
            elif last_connection == "z":
                occupied_connection = "-z"
            elif last_connection == "-z":
                occupied_connection = "z"

            last_coordinate = next_part.coordinates
            last_part_type = next_part.part_type
            connections = last_part_type.connections_per_axis()

            for connection in connections:
                if connection == occupied_connection:
                    continue

                pipe, new_part = self.create_part_and_pipe_for_connection(connection, last_coordinate, last_part_type)

                part_index += 1
                graph.add_node(part_index, pipe)
                graph.add_edge(part_index - 1, part_index)
                nb_pipes += 1

                if part_index - nb_pipes >= nb_parts:
                    return graph

                part_index += 1
                graph.add_node(part_index, new_part)
                graph.add_edge(part_index - 1, part_index)

                end_parts.append((new_part, connection))

        return graph

    def create_part_and_pipe_for_connection(self, connection, last_coordinate, last_part_type):
        pipe_type = random_pipe_type()
        destination_part_type = random_part_type()

        distance = -1 if "-" in connection else 1

        by_axis_origin = last_part_type.distance_per_axis()
        by_axis_pipe = pipe_type.distance_per_axis()
        by_axis_destination = destination_part_type.distance_per_axis()

        new_part_coordinates = last_coordinate
        pipe_coordinates = last_coordinate
        pipe_direction = np.asarray([0., 0., 0.])

        if "x" in connection:
            distance = distance * (by_axis_origin["x"] + by_axis_pipe["x"] + by_axis_destination["x"])
            new_part_coordinates[0] = new_part_coordinates[0] + distance

            pipe_coordinates[0] = by_axis_origin["x"] + by_axis_pipe["x"]
            pipe_direction[2] = np.pi / 2
        elif "y" in connection:
            distance = distance * (by_axis_origin["y"] + by_axis_pipe["y"] + by_axis_destination["y"])
            new_part_coordinates[1] = new_part_coordinates[1] + distance

            pipe_coordinates[1] = by_axis_origin["y"] + by_axis_pipe["y"]
            pipe_direction[0] = np.pi / 2
        elif "z" in connection:
            distance = distance * (by_axis_origin["z"] + by_axis_pipe["z"] + by_axis_destination["z"])
            new_part_coordinates[2] = new_part_coordinates[2] + distance

            pipe_coordinates[2] = by_axis_origin["z"] + by_axis_pipe["z"]

        pipe = PipelinePart(pipe_type, pipe_coordinates, pipe_direction, 1)
        new_part = PipelinePart(destination_part_type, new_part_coordinates, np.asarray([0., 0., 0.]), 1)

        return pipe, new_part

    def build_graph(self, point_cloud: PointCloud) -> PipelineGraph:
        assert point_cloud.is_classified()

        raise NotImplementedError("Not yet implemented")
