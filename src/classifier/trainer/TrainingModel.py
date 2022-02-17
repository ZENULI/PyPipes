import pathlib
import open3d as o3d

from src.core.PointCloud import PointCloud
from src.core.Point import Point
from src.graph_creator.core.PipelineGraph import PipelineGraph
from src.graph_creator.GraphCreator import GraphCreator
from src.pipeline_constructor.PipelineConstructor import PipelineConstructor

from copy import deepcopy


class TrainingModel:

    def __init__(self, pipeline_graph: PipelineGraph, nb_points_per_mesh: int = 50) -> None:
        resource_dir = pathlib.Path(__file__).parent.parent.parent.parent / "resources" / "3Dmodels"

        self._point_cloud_model = o3d.io.read_point_cloud(str(resource_dir / "empty.ply"))

        pipeline_constructor = PipelineConstructor()

        all_points = []

        for node in pipeline_graph.graph.nodes:
            part_type = pipeline_graph.graph.nodes[node]['type']
            coordinates = pipeline_graph.graph.nodes[node]['coordinates']
            direction = pipeline_graph.graph.nodes[node]['direction']

            mesh = pipeline_constructor.create_mesh(part_type, coordinates, direction)
            point_cloud = mesh.sample_points_uniformly(nb_points_per_mesh)

            for point in point_cloud.points:
                label_point = Point(point[0], point[1], point[2])

                label_point.part_type = part_type
                label_point.center = coordinates
                label_point.direction = direction
                label_point.radius = 1.

                all_points.append(label_point)

            self._point_cloud_model += point_cloud

        self._point_cloud_unlabelled = PointCloud(all_points)
        self._point_cloud_labelled = PointCloud(deepcopy(all_points))

        self._point_cloud_unlabelled.clear_labels()

    @property
    def point_cloud_model(self):
        return self._point_cloud_model

    @property
    def point_cloud_labelled(self):
        return self._point_cloud_labelled

    @@property
    def point_cloud_unlabelled(self):
        return self._point_cloud_unlabelled

    def visualize(self):
        o3d.visualization.draw_geometries([self._point_cloud_model])


def create_training_model(nb_parts: int = 50, nb_points_per_mesh: int = 50) -> TrainingModel:
    graph_creator = GraphCreator()
    pipeline_graph = graph_creator.create_random_graph(nb_parts)

    training_model = TrainingModel(pipeline_graph, nb_points_per_mesh)

    return training_model
