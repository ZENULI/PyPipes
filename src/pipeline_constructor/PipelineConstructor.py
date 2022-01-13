from src.pipeline_constructor.core.PipelineModel import PipelineModel
from src.graph_creator.core.PipelineGraph import PipelineGraph
from src.core.PartType import PartType


class PipelineConstructor:

    def __init__(self):
        self._part_dictionary = {PartType.PIPE: ""}

    def construct_pipeline(self, graph: PipelineGraph) -> PipelineModel:
        raise NotImplementedError("Not yet implemented")
