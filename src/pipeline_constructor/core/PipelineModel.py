from src.pipeline_constructor.core.Model3D import Model3D

import open3d as o3d


class PipelineModel:

    def __init__(self):
        self._elements = []

    @property
    def elements(self) -> list:
        return self._elements

    def add_element(self, element: Model3D) -> None:
        self._elements.append(element)

    def visualize(self) -> None:
        o3d.visualization.draw_geometries([element.mesh for element in self.elements])
