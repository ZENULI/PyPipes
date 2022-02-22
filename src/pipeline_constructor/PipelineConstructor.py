from src.pipeline_constructor.core.PipelineModel import PipelineModel
from src.pipeline_constructor.core.Model3D import Model3D
from src.graph_creator.core.PipelineGraph import PipelineGraph, PipelinePart
from src.core.PartType import PartType

import open3d as o3d
import numpy as np

from scipy.spatial.transform import Rotation as R


###########

def compute_rotation_matrix(axis, theta):

    '''    
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    https://en.wikipedia.org/wiki/Euler%E2%80%93Rodrigues_formula

    example : 

        >>> v = [3, 5, 0]
        >>> axis = [4, 4, 1]
        >>> theta = 1.2 

        >>> print(np.dot(rotation_matrix(axis, theta), v)) 
        # [ 2.74911638  4.77180932  1.91629719]
    '''

    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                    [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                    [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

#########


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
