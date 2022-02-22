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

import argparse
from src.graph_creator.GraphCreator import GraphCreator
from src.pipeline_constructor.PipelineConstructor import PipelineConstructor


def main(args):


    print("building model...")

    creator = GraphCreator()
    test_graph = creator.create_random_graph(10)
    constructor = PipelineConstructor()
    model = constructor.construct_pipeline(test_graph)
    model.visualize() 



if __name__ == '__main__':

    #input arguments

    parser = argparse.ArgumentParser()
    #parser.add_argument('--nb_models', type=str, required=True, help='input image for generating caption')
    #parser.add_argument('--encoder_path', type=str, default='models/encoder-5-3000.pkl', help='path for trained encoder')

    args = parser.parse_args()
    main(args)
