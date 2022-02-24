from src.graph_creator.core.PipelineGraph import PipelineGraph, PipelinePart
from src.pipeline_constructor.PipelineConstructor import PipelineConstructor
from src.core.PointCloud import PointCloud
from src.core.PartType import PartType

from src.core.PartType import random_part_type, random_pipe_type

import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
import pathlib


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

        save_path = 'scripts/output'
        resource_dir = pathlib.Path(__file__).parent.parent.parent

        full_graph = PipelineGraph()

        part_index = 0

        for label in PartType:
            list_points = []
            class_list_points = []
            list_points_coordinates = []

            # selectionner l'ensemble des points qui ont ce labels
            for j in range(0, len(point_cloud.points)):
                point = point_cloud.points[j]

                if point.part_type == label:
                    list_points.append(point.center)
                    class_list_points.append(point)
                    list_points_coordinates.append([point.x, point.y, point.z])

                array_points = np.array(list_points)
                array_points_world = np.array(list_points_coordinates)

            # en faire un nuage
            if list_points:
                class_pcd = o3d.geometry.PointCloud()
                class_pcd.points = o3d.utility.Vector3dVector(array_points)

                class_pcd_world = o3d.geometry.PointCloud()
                class_pcd_world.points = o3d.utility.Vector3dVector(array_points_world)
                
                # DBSCAN sur ce nuage (doit contenir au moins min_points et à moins de 2 m de distance)
                with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
                    labels_ = np.array(class_pcd.cluster_dbscan(eps=1.1, min_points=15, print_progress=True))

                max_label = labels_.max()

                print(f"label {str(label)} has {max_label} clusters of lengths :")

                colors = plt.get_cmap("tab20")(labels_ / (max_label if max_label > 0 else 1))
                colors[labels_ < 0] = 0
                class_pcd_world.colors = o3d.utility.Vector3dVector(colors[:, :3])

                class_pcd_path = resource_dir / save_path / (str(label) + "_pcd.ply")

                o3d.io.write_point_cloud(str(class_pcd_path), class_pcd_world)



                # sur chaque cluster de ce nuage :
                for k in range(0, max_label + 1):
                    cluster_types = []
                    cluster_x = []
                    cluster_y = []
                    cluster_z = []
                    cluster_radius = []
                    cluster_vx = []
                    cluster_vy = []
                    cluster_vz = []

                    length_cluster = 0

                    for j in range(0, len(class_pcd.points)):
                        point = class_list_points[j]

                        if labels_[j] == k:  # selection des points du cluster
                            cluster_types.append(point.part_type)

                            cluster_x.append(point.center[0])
                            cluster_y.append(point.center[1])
                            cluster_z.append(point.center[2])

                            cluster_vx.append(point.direction[0])
                            cluster_vy.append(point.direction[1])
                            cluster_vz.append(point.direction[2])

                            cluster_radius.append(point.radius)

                            length_cluster += 1

                    new_center = np.asarray([np.mean(cluster_x), np.mean(cluster_y), np.mean(cluster_z)])
                    new_direction = np.asarray([np.mean(cluster_vx), np.mean(cluster_vy), np.mean(cluster_vz)])
                    new_type = max(set(cluster_types), key=cluster_types.count)

                    # ajouter la part correspondante au cluster
                    new_part = PipelinePart(new_type, new_center, new_direction, 1)
                    full_graph.add_node(part_index, new_part)
                    part_index += 1

        return full_graph
