from src.graph_creator.core.PipelineGraph import PipelineGraph
from src.core.PointCloud import PointCloud


class GraphCreator:

    def __init__(self):
        pass

    def build_graph(self, point_cloud: PointCloud) -> PipelineGraph:
        assert point_cloud.is_classified()

        raise NotImplementedError("Not yet implemented")
