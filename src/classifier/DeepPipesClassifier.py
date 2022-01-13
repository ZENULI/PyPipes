from src.classifier.Classifier import Classifier
from src.classifier.core.CNNModel import CNNModel
from src.core.PointCloud import PointCloud


class DeepPipesClassifier(Classifier):

    def __init__(self):
        self._model = None

    def classify(self, point_cloud: PointCloud) -> PointCloud:
        raise NotImplementedError("Not yet implemented")

    def is_trained(self) -> bool:
        return self._model and type(self._model) == CNNModel

    @property
    def model(self) -> CNNModel:
        return self._model

    @model.setter
    def model(self, value: CNNModel) -> None:
        self._model = value
