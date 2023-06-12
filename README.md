# Simple DataOps Docker

## Prerequisites

- Install [docker](https://docs.docker.com/engine/install/).

## Preparation

Install Python 3.10 on [Pyenv](https://github.com/pyenv/pyenv#installation) or [Anaconda](https://docs.anaconda.com/anaconda/install/index.html) and execute the following commands:

```bash
$ make init     # setup packages (need only once)
```

## How To Play

### 1. Create Infra

```bash
$ make compose          # create all the containers (need only once)
```

You can delete the containers.

```bash
$ make compose-clean    # delete the containers
```

### 2. TBD

## For Developers

```bash
$ make check          # all static analysis scripts
$ make format         # format scripts
$ make lint           # lints scripts
```
