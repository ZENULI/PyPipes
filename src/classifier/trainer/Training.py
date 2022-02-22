import os.path as osp
import numpy as np

import wandb
import torch
import pathlib

from torch_geometric.data import Dataset, Data
from torch_points3d.datasets.base_dataset import BaseDataset
from torch_points3d.metrics.classification_tracker import ClassificationTracker

from src.classifier.trainer.TrainingModel import TrainingModel

from os import listdir


class GlobalDataset(BaseDataset):

    def __init__(self):
        super().__init__()

        resource_dir = pathlib.Path(__file__).parent.parent.parent / "resources" / "data"

        self.train_dataset = PipelineDataset(str(resource_dir / "training"), for_labels=True)
        self.test_dataset = PipelineDataset(str(resource_dir / "tests"), for_labels=False)

    def get_tracker(self, wandb_log: bool, tensorboard_log: bool = False):
        return ClassificationTracker(self, wandb_log=wandb_log, use_tensorboard=tensorboard_log)


class PipelineDataset(Dataset):

    def __init__(self, root, transform=None, pre_transform=None, pre_filter=None, for_labels=True):
        self._files = [f for f in listdir(osp.join(root, "raw")) if osp.isfile(osp.join(root, "raw", f))]
        self._for_labels = for_labels

        super().__init__(root, transform, pre_transform, pre_filter)

    @property
    def raw_file_names(self):
        return self._files

    @property
    def processed_file_names(self):
        return [osp.splitext(f)[0] + "_label" + ".pt" if self._for_labels
                else osp.splitext(f)[0] + "_geometry" + ".pt" for f in self._files]

    def process(self):
        idx = 0
        for raw_path in self.raw_paths:
            model = TrainingModel(json_file=raw_path).point_cloud_labelled

            x = np.zeros((len(model.points), 3)) if self._for_labels else np.zeros((len(model.points), 4))
            y = np.zeros(len(model.points)) if self._for_labels else np.zeros((len(model.points), 6))

            for i in range(0, len(model.points)):
                point = model.points[i]

                x[i][0] = point.x
                x[i][1] = point.y
                x[i][2] = point.z

                if not self._for_labels:
                    x[i][3] = point.part_type.value

                if self._for_labels:
                    y[i] = point.part_type.value
                else:
                    y[i][0] = point.center[0]
                    y[i][1] = point.center[1]
                    y[i][2] = point.center[2]

                    y[i][0] = point.direction[0]
                    y[i][1] = point.direction[1]
                    y[i][2] = point.direction[2]

            data = Data(x=x, y=y)

            if self.pre_filter is not None and not self.pre_filter(data):
                continue

            if self.pre_transform is not None:
                data = self.pre_transform(data)

            torch.save(data, osp.join(self.processed_dir, f'data_{idx}.pt'))
            idx += 1

    def len(self):
        return len(self.processed_file_names)

    def get(self, idx):
        data = torch.load(osp.join(self.processed_dir, f'data_{idx}.pt'))
        return data


if __name__ == '__main__':
    wandb.init(project="PyPipes", entity="Kodvir")

    wandb.config = {
        "learning_rate": 0.001,
        "epochs": 100,
        "batch_size": 128
    }
