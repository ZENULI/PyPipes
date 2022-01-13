import abc

from src.core import PointCloud


class Classifier(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def classify(self, point_cloud: PointCloud) -> PointCloud:
        pass
