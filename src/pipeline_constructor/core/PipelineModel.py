from src.pipeline_constructor.core.Model3D import Model3D

import open3d as o3d
import pathlib


class PipelineModel:

    def __init__(self):
        resource_dir = pathlib.Path(__file__).parent.parent.parent.parent / "resources" / "3Dmodels"
        self._main_mesh = o3d.io.read_triangle_mesh(str(resource_dir / "empty.ply"))

    @property
    def mesh(self):
        return self._main_mesh

    def add_element(self, element: Model3D) -> None:
        self._main_mesh += element.mesh

    def compute_normals(self):
        self._main_mesh.compute_vertex_normals()

    def save(self, filepath: pathlib.Path, extension=".ply") -> None:
        o3d.io.write_triangle_mesh(str(filepath) + extension, self._main_mesh)

    def visualize(self) -> None:
        box = self._main_mesh.get_axis_aligned_bounding_box()
        box.color = (1, 0, 0)

        mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1, origin=[0, 0, 0])

        o3d.visualization.draw_geometries([self._main_mesh, mesh_frame, box])
