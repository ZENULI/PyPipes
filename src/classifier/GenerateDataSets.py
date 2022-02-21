import pathlib
import random

from src.classifier.trainer.TrainingModel import TrainingModel, create_training_model


if __name__ == '__main__':
    resource_dir = pathlib.Path(__file__).parent.parent.parent / "resources" / "data"

    nb_models = 100
    for sub_folder in ["tests", "training", "validation"]:
        for i in range(0, nb_models):
            file_path = resource_dir / sub_folder / ("TrainingData_" + str(i) + ".json")

            nb_parts = random.randrange(25, 100)
            sampling = random.randrange(25, 100)

            model = create_training_model(nb_parts=nb_parts, nb_points_per_mesh=sampling)

            model.save_model(str(file_path))
