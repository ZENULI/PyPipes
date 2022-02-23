import argparse
import random
import pathlib
import sys
sys.path.append('../PyPipes')

import open3d as o3d

from src.core.PartType import PartType, random_part_type, random_pipe_type
from src.classifier.trainer.TrainingModel import create_training_model

from src.graph_creator.GraphCreator import GraphCreator
from src.pipeline_constructor.PipelineConstructor import PipelineConstructor

from copy import deepcopy

save_path = 'scripts/output'
resource_dir = pathlib.Path(__file__).parent.parent

pcd_truth_path = resource_dir / save_path / "pcd_truth.ply"
labels_truth_path = resource_dir / save_path / "labels_truth.json"
mesh_truth_path = resource_dir / save_path / "mesh_truth.ply"

labels_classif_path = resource_dir / save_path / "labels_classif.json"
mesh_reconst_path = resource_dir / save_path / "mesh_reconst"


def labelled_pcd_write(pcd: list, file_path: str):

    import json
    from src.core.PartType import EnumEncoder, as_part_type
    data = []
    for point in pcd:
        data.append({
            "point_coordinates": [point.x, point.y, point.z],
            "part_center": [point.center[0], point.center[1], point.center[2]],
            "part_type": point.part_type,
            "direction": [point.direction[0], point.direction[1], point.direction[2]],
            "radius": point.radius
        })
    json_data = {"points": data}
    json_string = json.dumps(json_data, cls=EnumEncoder)

    with open(file_path, 'w') as outfile:
        json.dump(json_string, outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generates a random pipeline and try to reconstruct it after shuffling")

    parser.add_argument('--nbParts', type=int, default=10, help='Number of parts used in the generated Pipeline')
    parser.add_argument('--sampling', type=int, default=100, help='Number of points generated per pipeline part')
    parser.add_argument('--simulatedAccuracy', type=float, default=0.95,
                        help='Simulated classification accuracy (Percentage between 0 and 1)')
    parser.add_argument('--simulatedCenterError', type=float, default=0.05,
                        help='Simulated error on part center characteristic (Percentage between 0 and 1)')
    parser.add_argument('--simulatedDirectionError', type=float, default=0.05,
                        help='Simulated error on direction characteristic (Percentage between 0 and 1)')
    parser.add_argument('--saveFileName', type=str, default="ReconstructedGraph",
                        help="Name of the file in which to store the reconstructed pipeline")
    parser.add_argument('--visualiseResult', type=bool, default=True,
                        help='If true, visualise the reconstructed pipeline')

    args = parser.parse_args()

    nb_parts = args.nbParts
    sampling = args.sampling

    file_name = args.saveFileName
    visualise_result = args.visualiseResult

    model = create_training_model(nb_parts=nb_parts, nb_points_per_mesh=sampling)
    
    labels_truth_points = deepcopy(model.point_cloud_labelled.points)
    labelled_pcd_write(labels_truth_points, str(labels_truth_path)) 
    model.save_mesh(str(mesh_truth_path))
    model.save_pcd(str(pcd_truth_path))

    # Simulate classification
    simulated_accuracy = args.simulatedAccuracy
    simulated_center_error = args.simulatedCenterError
    simulated_direction_error = args.simulatedDirectionError

    classification = deepcopy(model.point_cloud_unlabelled)

    assert 0 <= simulated_accuracy <= 1
    assert 0 <= simulated_center_error <= 1
    assert 0 <= simulated_direction_error <= 1

    for i in range(0, len(classification.points)):
        ground_truth = model.point_cloud_labelled.points[i]

        # Jumble part_type
        prob = random.randrange(0, 100)
        if prob >= simulated_accuracy * 100:
            error_part_type = ground_truth.part_type

            while error_part_type == ground_truth.part_type:
                if ground_truth.part_type in [PartType.PIPE_1, PartType.PIPE_2, PartType.PIPE_3, PartType.PIPE_4]:
                    error_part_type = random_pipe_type()
                else:
                    error_part_type = random_part_type()

            classification.points[i].part_type = error_part_type
        else:
            classification.points[i].part_type = ground_truth.part_type

        center_error = random.uniform(-simulated_center_error, simulated_center_error)
        direction_error = random.uniform(-simulated_direction_error, simulated_direction_error)

        classification.points[i].center = ground_truth.center + ground_truth.center * center_error
        classification.points[i].direction = ground_truth.direction + ground_truth.direction * direction_error
        classification.points[i].radius = 1.
   
    labelled_pcd_write(classification.points, str(labels_classif_path)) 

    graph_creator = GraphCreator()
    pipeline_constructor = PipelineConstructor()
    
    reconstructed_graph = graph_creator.build_graph(classification)
    reconstructed_model = pipeline_constructor.construct_pipeline(reconstructed_graph)
    reconstructed_model.save(mesh_reconst_path)

    if visualise_result:
        reconstructed_model.visualize()


