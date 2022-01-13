#### 1. Build the environnement image

```bash
$ wget https://raw.githubusercontent.com/seb2s/CHDO/main/docker/Dockerfile?token=GHSAT0AAAAAABOKBZGG4WVAPDTMWZFJMOFCYOYFAKQ
$ docker build -t project_name
```
#### 2. Run the container

```bash
$ docker run -it --entryppoint bash project_name
```

#### 3. In the container 

```bash
$ git clone https://github.com/seb2s/CHDO/blob/main/docker/Dockerfile
$ cd CHDO
$ python3 setup.py test
```