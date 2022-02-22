"""
# This files originate from the "PyPipes" project:
#   https://github.com/ZENULI/PyPipes
# Created by ZENULI at University Paul Sabatier III :
#   https://github.com/BastienKovac
#   https://github.com/Ulynor
#   https://github.com/seb2s
# License:
#   MIT License Copyright (c) 2022 ZENULI
"""

import sys
sys.path.append('../PyPipes')

import pathlib
import random
import argparse
from src.classifier.trainer.TrainingModel import TrainingModel, create_training_model
from src.graph_creator.GraphCreator import GraphCreator
from src.pipeline_constructor.PipelineConstructor import PipelineConstructor


# PARAMETERS TO MODIFY
nb_models = 30
nb_min_part = 5
nb_max_part = 15
nb_points_per_mesh = 128
save_path = 'resources/results'


def main(args):

    print("building samples...")

    #resource_dir = pathlib.Path(__file__).parent.parent.parent / "resources" / "data"
    resource_dir = pathlib.Path(__file__).parent.parent.parent

    for i in range(0, nb_models):
        file_path = resource_dir / save_path / (str(i) + "_classif.json")
        mesh_path = resource_dir / save_path / (str(i) + "_mesh.ply")
        pcd_path = resource_dir / save_path / (str(i) + "_pcd.ply")

        nb_parts = random.randrange(nb_min_part, nb_max_part)

        #model = create_training_model(nb_parts=nb_parts, nb_points_per_mesh=sampling)

        graph_creator = GraphCreator()
        pipeline_graph = graph_creator.create_random_graph(nb_parts)

        model = TrainingModel(pipeline_graph, nb_points_per_mesh)
        model.save_model(str(file_path))
        model.save_mesh(str(mesh_path))
        model.save_pcd(str(pcd_path))
        #model.save_graph(_)

if __name__ == '__main__':

    #input arguments

    parser = argparse.ArgumentParser()
    #parser.add_argument('--nb_models', type=str, required=True, help='input image for generating caption')
    #parser.add_argument('--encoder_path', type=str, default='models/encoder-5-3000.pkl', help='path for trained encoder')

    args = parser.parse_args()
    main(args)
