import argparse


def main(args):

    """Do stuff"""

if __name__ == '__main__':
    """input arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph', type=str, required=True, help='input graph for generating 3D model')
    #parser.add_argument('--encoder_path', type=str, default='models/encoder-5-3000.pkl', help='path for trained encoder')

    args = parser.parse_args()
    main(args)
