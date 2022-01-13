## Usage

#### 1. Build the environnement image

```bash
$ wget https://raw.githubusercontent.com/ZENULI/PyPipes/main/docker/Dockerfile
$ docker build -t Pypipes
```
#### 2. Run the container

```bash
$ docker run -it --entryppoint bash Pypipes
```

#### 3. In the container 

```bash
$ cd Pypipes
$ python3 setup.py test
```

###### To delete the container : 

```bash
$ exit
$ docker stop Pypipes
$ docker rm -f Pypipes
```