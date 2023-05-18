# Simple DataOps Docker

## Prerequisites

- Install [docker](https://docs.docker.com/engine/install/).

## Preparation

Install [Pyenv](https://github.com/pyenv/pyenv#installation) or [Anaconda](https://docs.anaconda.com/anaconda/install/index.html) and execute the following commands:

```bash
$ make init     # setup packages (need only once)
```

## How To Play

### 1. Build Image

```bash
$ make build-image          # build an airflow image (need only once)
```

You can remove the airflow image.

```bash
$ make build-image-clean    # remove the airflow image
```

### 2. Create Infra

```bash
$ make compose          # create all containers (need only once)
```

You can delete the containers.

```bash
$ make compose-clean    # delete the containers
```

### 3. TBD

## For Developers

```bash
$ make check          # all static analysis scripts
$ make format         # format scripts
$ make lint           # lints scripts
```
