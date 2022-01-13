from src.graph_creator.core.PipelineGraph import PipelineGraph
from src.classifier.core.CNNModel import CNNModel


class Trainer:

    def __init__(self):
        pass

    def train_model(self, pipeline_graph: PipelineGraph) -> CNNModel:
        raise NotImplementedError("Not yet implemented")
