import open3d as o3d


class Model3D:

    def __init__(self, mesh: o3d.geometry.TriangleMesh) -> None:
        self._mesh = mesh

    @property
    def mesh(self) -> o3d.geometry.TriangleMesh:
        return self._mesh
