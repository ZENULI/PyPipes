from src.pipeline_constructor.core.PipelineModel import PipelineModel
from src.pipeline_constructor.core.Model3D import Model3D
from src.graph_creator.core.PipelineGraph import PipelineGraph, PipelinePart
from src.core.PartType import PartType

import open3d as o3d
import numpy as np


class PipelineConstructor:

    def __init__(self):
        self._part_dictionary = {part_type: part_type.part_model_file() for part_type in PartType}

    def construct_pipeline(self, pipeline: PipelineGraph) -> PipelineModel:
        graph = pipeline.graph
        model = PipelineModel()

        for node in graph.nodes:
            part_type = graph.nodes[node]['type']
            coordinates = graph.nodes[node]['coordinates']
            direction = graph.nodes[node]['direction']

            part = Model3D(self.create_mesh(part_type, coordinates, direction))

            model.add_element(part)

        model.compute_normals()

        return model

    def create_mesh_from_part(self, part: PipelinePart) -> o3d.geometry.TriangleMesh:
        return self.create_mesh(part.part_type, part.coordinates, part.direction)

    def create_mesh(self, part_type: PartType, coordinates: np.ndarray,
                    direction: np.ndarray) -> o3d.geometry.TriangleMesh:

        mesh = o3d.io.read_triangle_mesh(str(self._part_dictionary[part_type]))

        rotation = o3d.geometry.get_rotation_matrix_from_xyz(direction)

        mesh.translate([0., 0., 0.], relative=True)
        mesh.rotate(rotation, center=[0., 0., 0.])
        mesh.translate(coordinates, relative=True)

        return mesh
