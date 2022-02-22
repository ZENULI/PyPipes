from src.graph_creator.core.PipelineGraph import PipelineGraph
from src.classifier.core.CNNModel import CNNModel
from src.classifier.trainer.TrainingModel import TrainingModel

import torch
from torch.utils.data import Dataset

from os import listdir
from os.path import isfile, join


class Trainer:

    def __init__(self):
        pass

    def train_model(self, pipeline_graph: PipelineGraph) -> CNNModel:
        raise NotImplementedError("Not yet implemented")


class PipelineDataset(Dataset):

    def __init__(self, root_dir: str, transform=None) -> None:
        self.file_names = [join(root_dir, f) for f in listdir(root_dir) if isfile(join(root_dir, f))]
        self.transform = transform

    def __len__(self):
        return len(self.file_names)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.toist()

        return TrainingModel(json_file=self.file_names[idx])

