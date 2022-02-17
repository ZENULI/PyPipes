from src.graph_creator.core.PipelineGraph import PipelineGraph, PipelinePart
from src.pipeline_constructor.PipelineConstructor import PipelineConstructor
from src.core.PointCloud import PointCloud
from src.core.PartType import PartType

from src.core.PartType import random_part_type, random_pipe_type

import numpy as np
import open3d as o3d


def intersects(a: o3d.geometry.AxisAlignedBoundingBox, b: o3d.geometry.AxisAlignedBoundingBox) -> bool:
    a_max = a.get_max_bound()
    a_min = a.get_min_bound()

    b_max = b.get_max_bound()
    b_min = b.get_min_bound()

    margin = 0.1

    return (a_min[0] + margin <= b_max[0] and a_max[0] >= b_min[0] + margin) and \
           (a_min[1] + margin <= b_max[1] and a_max[1] >= b_min[1] + margin) and \
           (a_min[2] + margin <= b_max[2] and a_max[2] >= b_min[2] + margin)


class GraphCreator:

    def __init__(self):
        pass

    def create_random_graph(self, nb_parts: int) -> PipelineGraph:
        graph = PipelineGraph()
        pipeline_constructor = PipelineConstructor()

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

        bounding_boxes = [pipeline_constructor.create_mesh_from_part(part).get_axis_aligned_bounding_box()]

        end_parts = []

        for connection in connections:
            pipe, new_part = self.create_part_and_pipe_for_connection(connection, last_coordinate, last_part_type)

            part_index += 1
            graph.add_node(part_index, pipe)
            graph.add_edge(part_index - 1, part_index)
            nb_pipes += 1

            bounding_boxes.append(pipeline_constructor.create_mesh_from_part(pipe).get_axis_aligned_bounding_box())
            bounding_boxes.append(pipeline_constructor.create_mesh_from_part(new_part).get_axis_aligned_bounding_box())

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

            occupied_connection = self.opposite_connection(last_connection)

            last_coordinate = next_part.coordinates
            last_part_type = next_part.part_type
            last_direction = next_part.direction
            connections = last_part_type.connections_per_axis()

            for connection in connections:
                if (last_direction[1] != 0 and "x" in connection) or \
                        (last_direction[2] != 0 and "y" in connection) or \
                        (last_direction[0] != 0 and "z" in connection):
                    connection = self.opposite_connection(connection)

                if connection == occupied_connection:
                    continue

                pipe, new_part = self.create_part_and_pipe_for_connection(connection, last_coordinate, last_part_type)

                pipe_bounding_box = pipeline_constructor.create_mesh_from_part(pipe).get_axis_aligned_bounding_box()
                part_bounding_box = pipeline_constructor.create_mesh_from_part(new_part).get_axis_aligned_bounding_box()

                pipe_intersects = False
                part_intersects = False

                for bounding_box in bounding_boxes:
                    pipe_intersects = intersects(bounding_box, pipe_bounding_box) or pipe_intersects
                    part_intersects = intersects(bounding_box, part_bounding_box) or part_intersects

                    if pipe_intersects and part_intersects:
                        break

                if not pipe_intersects:
                    part_index += 1
                    graph.add_node(part_index, pipe)
                    graph.add_edge(part_index - 1, part_index)
                    bounding_boxes.append(pipe_bounding_box)
                    nb_pipes += 1

                    if part_index - nb_pipes >= nb_parts:
                        return graph

                if not pipe_intersects and not part_intersects:
                    part_index += 1
                    graph.add_node(part_index, new_part)
                    graph.add_edge(part_index - 1, part_index)
                    bounding_boxes.append(part_bounding_box)

                    end_parts.append((new_part, connection))

        return graph

    def opposite_connection(self, last_connection):
        if last_connection == "x":
            return "-x"
        elif last_connection == "-x":
            return "x"
        elif last_connection == "y":
            return "-y"
        elif last_connection == "-y":
            return "y"
        elif last_connection == "z":
            return "-z"
        elif last_connection == "-z":
            return "z"

    def create_part_and_pipe_for_connection(self, connection, last_coordinate, last_part_type):
        pipe_type = random_pipe_type()
        destination_part_type = random_part_type()

        by_axis_origin = last_part_type.distance_per_axis()
        by_axis_pipe = pipe_type.distance_per_axis()
        by_axis_destination = destination_part_type.distance_per_axis()

        new_part_coordinates = np.copy(last_coordinate)
        new_part_direction = np.asarray([0., 0., 0.])
        pipe_direction = np.asarray([0., 0., 0.])
        pipe_coordinates = np.copy(new_part_coordinates)

        fixed_connection = connection
        destination_connections = destination_part_type.connections_per_axis()

        if connection in destination_connections \
                and self.opposite_connection(connection) not in destination_connections:
            if "x" in fixed_connection:
                new_part_direction[1] = np.pi / 2 if destination_part_type == PartType.ANGLE else np.pi
            elif "y" in fixed_connection:
                new_part_direction[2] = np.pi
            elif "z" in fixed_connection:
                new_part_direction[0] = np.pi

        distance_factor = -1 if "-" in fixed_connection else 1

        if "x" in fixed_connection:
            distance = distance_factor * (by_axis_origin["x"] + (by_axis_pipe["z"] * 2) + by_axis_destination["x"])
            new_part_coordinates[0] = new_part_coordinates[0] + distance

            pipe_coordinates[0] = pipe_coordinates[0] + distance_factor * (by_axis_origin["x"] + by_axis_pipe["z"])
            pipe_direction[1] = np.pi / 2
        elif "y" in fixed_connection:
            distance = distance_factor * (by_axis_origin["y"] + (by_axis_pipe["z"] * 2) + by_axis_destination["y"])
            new_part_coordinates[1] = new_part_coordinates[1] + distance

            pipe_coordinates[1] = pipe_coordinates[1] + distance_factor * (by_axis_origin["y"] + by_axis_pipe["z"])
            pipe_direction[0] = np.pi / 2
        elif "z" in fixed_connection:
            distance = distance_factor * (by_axis_origin["z"] + (by_axis_pipe["z"] * 2) + by_axis_destination["z"])
            new_part_coordinates[2] = new_part_coordinates[2] + distance

            pipe_coordinates[2] = pipe_coordinates[2] + distance_factor * (by_axis_origin["z"] + by_axis_pipe["z"])

        pipe = PipelinePart(pipe_type, pipe_coordinates, pipe_direction, 1)
        new_part = PipelinePart(destination_part_type, new_part_coordinates, new_part_direction, 1)

        return pipe, new_part

    def build_graph(self, point_cloud: PointCloud) -> PipelineGraph:
        assert point_cloud.is_classified()

        raise NotImplementedError("Not yet implemented")
