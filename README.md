# Simple DataOps K8s

## Prerequisites

- Install [docker](https://docs.docker.com/engine/install/).
- Install [Minikube](https://minikube.sigs.k8s.io/docs/start/).
- Install [Helm](https://helm.sh/docs/intro/install/).

## Preparation

Install [Anaconda](https://docs.anaconda.com/anaconda/install/index.html) and execute the following commands:

```bash
$ make env       # create a conda environment (need only once)
$ conda activate simple-dataops-k8s
$ make init      # setup packages (need only once)
```

## How To Play

### K8s Cluster Setup

```bash
$ make cluster          # create a k8s cluster (need only once)
```

You can delete the k8s cluster.

```bash
$ make cluster-clean    # delete the k8s cluster
```

### TBD

## For Developers

```bash
$ make check          # all static analysis scripts
$ make format         # format scripts
$ make lint           # lints scripts
```
