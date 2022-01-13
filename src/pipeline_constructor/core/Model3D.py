from open3d.cpu.pybind.geometry.TriangleMesh import TriangleMesh


class Model3D:

    def __init__(self, mesh: TriangleMesh):
        self._mesh = mesh

    @property
    def mesh(self) -> TriangleMesh:
        return self._mesh
