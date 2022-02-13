from src.pipeline_constructor.core.PipelineModel import PipelineModel
from src.pipeline_constructor.core.Model3D import Model3D
from src.graph_creator.core.PipelineGraph import PipelineGraph
from src.core.PartType import PartType

import pathlib
import random

import open3d as o3d


class PipelineConstructor:

    def __init__(self):
        resource_dir = pathlib.Path(__file__).parent.parent.parent / "resources" / "3Dmodels"

        self._part_dictionary = {part_type: part_type.part_model_file() for part_type in PartType}
        self._pipes = [resource_dir / "pipe1.obj", resource_dir / "pipe2.obj", resource_dir / "pipe3.obj"]

    def construct_pipeline(self, pipeline: PipelineGraph) -> PipelineModel:
        def get_pipe():
            return self._pipes[random.randrange(0, len(self._pipes))]

        graph = pipeline.graph
        model = PipelineModel()

        for node in graph.nodes:
            mesh = o3d.io.read_triangle_mesh(str(self._part_dictionary[graph.nodes[node]['type']]))
            mesh.compute_vertex_normals()

            part_model = Model3D(mesh)

            # Center the part then put it at its final coordinates
            part_model.mesh.translate([0, 0, 0])
            coordinates = graph.nodes[node]['coordinates']
            part_model.mesh.translate(coordinates)

            # Rotate part in appropriate direction
            r = o3d.geometry.get_rotation_matrix_from_axis_angle(graph.nodes[node]['direction'])
            part_model.mesh.rotate(r, center=graph.nodes[node]['coordinates'])

            # Scale the part to appropriate size
            part_model.mesh.scale(graph.nodes[node]['radius'], center=graph.nodes[node]['coordinates'])

            model.add_element(part_model)

        return model
