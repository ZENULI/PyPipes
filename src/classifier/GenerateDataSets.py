import pathlib
import random

from src.classifier.trainer.TrainingModel import TrainingModel, create_training_model


if __name__ == '__main__':
    resource_dir = pathlib.Path(__file__).parent.parent.parent / "resources" / "data"

    ''''for i in range(0, 700):
        file_path = resource_dir / "training" / ("TrainingData_" + str(i) + ".json")

        nb_parts = random.randrange(50, 150)
        sampling = random.randrange(50, 150)

        model = create_training_model(nb_parts=nb_parts, nb_points_per_mesh=sampling)

        model.save_model(str(file_path))'''''

    for i in range(0, 30):
        file_path = resource_dir / "tests" / ("TrainingData_" + str(i) + ".json")

        nb_parts = random.randrange(5, 15)
        #sampling = random.randrange(500, 1500)
        sampling = 1048

        model = create_training_model(nb_parts=nb_parts, nb_points_per_mesh=sampling)

        model.save_model(str(file_path))
