from src.pipeline_constructor.core.Model3D import Model3D


class PipelineModel:

    def __init__(self):
        self._elements = []

    @property
    def elements(self) -> list:
        return self._elements

    def add_element(self, element: Model3D) -> None:
        self._elements.append(element)
