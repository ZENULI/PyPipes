from src.pipeline_constructor.core.PipelineModel import PipelineModel
from src.pipeline_constructor.core.Model3D import Model3D
from src.graph_creator.core.PipelineGraph import PipelineGraph
from src.core.PartType import PartType

import open3d as o3d


class PipelineConstructor:

    def __init__(self):
        self._part_dictionary = {part_type: part_type.part_model_file() for part_type in PartType}

    def construct_pipeline(self, pipeline: PipelineGraph) -> PipelineModel:
        graph = pipeline.graph
        model = PipelineModel()

        for node in graph.nodes:
            mesh = o3d.io.read_triangle_mesh(str(self._part_dictionary[graph.nodes[node]['type']]))

            coordinates = graph.nodes[node]['coordinates']
            direction = graph.nodes[node]['direction']

            rotation = o3d.geometry.get_rotation_matrix_from_xyz(direction)

            mesh.translate([0., 0., 0.], relative=True)
            mesh.rotate(rotation, center=coordinates)
            mesh.translate(coordinates, relative=True)

            part = Model3D(mesh)

            model.add_element(part)

        model.compute_normals()

        return model
