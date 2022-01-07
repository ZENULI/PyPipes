<img src="docs/source/_static/img/project_logo.png" alt="drawing" width="250"/>


**[Documentation]()** | **[Paper](https://doi.org/10.1016/j.gmod.2020.101079)** | **[Colab Notebooks](https://drive.google.com/drive/folders/1InpU4yZAYGR9_NB4wSGDx7t2d6K2b9zy?usp=sharing)** | **[Video Tutorials](https://www.youtube.com)** | **[Master Degree website](https://departement-informatique.univ-tlse3.fr/master-igai/)** 


**This project** is a [PyTorch](https://pytorch.org/) implementation of *DeepPipes: Learning 3D pipelines reconstruction from point clouds. Lili Cheng, Zhuo Wei, Mingchao Sun, Shiqing Xin, Andrei Sharf, Yangyan Li, Baoquan Chen, Changhe Tu. Graphical Models, Volume 111, 2020,*. 

It allows to reconstruct a 3d pipe model from a points cloud.

```
#### Abstract

Pipes are the basic building block in many industrial sites like electricity and chemical plants. Although
pipes are merely cylindrical primitives which can be defined by axis and radius, they often consist of
additional components like flanges, valves, elbows, tees, etc. 3D pipes are typically dense, consisting of a
wide range of topologies and geometries, with large self-occlusions. Thus, reconstruction of a coherent 3D pipe
models from large-scale point clouds is a challenging problem. In this work we take a prior-based
reconstruction approach which reduces the complexity of the general pipe reconstruction problem into a
combination of part detection and model fitting problems. We utilize convolutional network to learn point cloud
features and classify points into various classes, then apply robust clustering and graph-based aggregation
techniques to compute a coherent pipe model. Our method shows promising results on pipe models with varying
complexity and density both in synthetic and real cases.

Keywords: Point cloud, Pipes reconstruction, Convo-
lution network, Skeleton extraction

```

## Architecture Overview

<img src="docs/source/_static/img/project_architecture.png" alt="drawing" height="400"/>

**TODO**

## Neural Network 

<img src="docs/source/_static/img/nn_architecture.png" alt="drawing" height="400"/>

**TODO**


## Using this project (how to)

**TODO**

### Manage experiments with GraphGym

GraphGym allows you to manage and launch GNN experiments, using a highly modularized pipeline (see [here](https://pytorch-geometric.readthedocs.io/en/latest/notes/graphgym.html) for the accompanying tutorial).

```
git clone https://github.com/pyg-team/pytorch_geometric.git
cd pytorch_geometric/graphgym
bash run_single.sh  # run a single GNN experiment (node/edge/graph-level)
bash run_batch.sh   # run a batch of GNN experiments, using differnt GNN designs/datasets/tasks
```

Users are highly encouraged to check out the [documentation](https://pytorch-geometric.readthedocs.io/en/latest), which contains additional tutorials on the essential functionalities of PyG, including data handling, creation of datasets and a full list of implemented methods, transforms, and datasets.
For a quick start, check out our [examples](https://github.com/pyg-team/pytorch_geometric/tree/master/examples) in `examples/`.


## Installation

**Warning:** We do not recommend installation of the environnement as a root user on your system Python. Please setup a Anaconda or Miniconda environment or create a Docker image.

|             | `cpu` | `cu102` | `cu113` |
|-------------|-------|---------|---------|
| **Linux**   | ✅    | ✅      | ✅      |
| **Windows** |       |         |         |
| **macOS**   |       |         |         |

### Docker

Build the environnement image.

```
wget https://raw.githubusercontent.com/seb2s/CHDO/main/docker/Dockerfile?token=GHSAT0AAAAAABOKBZGG4WVAPDTMWZFJMOFCYOYFAKQ
docker build -t project_name
```
Run the container.

```
docker run -it --entryppoint bash project_name
```

In the container 

```
git clone https://github.com/seb2s/CHDO/blob/main/docker/Dockerfile
cd CHDO
python3 setup.py test
```
**TODO :**
* Compléter le Dockerfile avec le reste des librairies
* ajouter d'autres test (tester l'installation de toutes les libs)

### Anaconda

**TODO**

### From master

## Requirements

```

```

**TODO**

### Testing

You can run tests by running `pytest` in the root, or by running `python3 setup.py test`. Code coverage is enabled with pytest-cov.
You can find some more tests under the `testing/` folder!

## License

**TODO**


<img src="docs/source/_static/img/universite_logo.png" alt="drawing" width="200"/>
