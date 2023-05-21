# Simple DataOps Docker

## Prerequisites

- Install [docker](https://docs.docker.com/engine/install/).

## Preparation

Install [Pyenv](https://github.com/pyenv/pyenv#installation) or [Anaconda](https://docs.anaconda.com/anaconda/install/index.html) and execute the following commands:

```bash
$ make init     # setup packages (need only once)
```

## How To Play

### 1. Infra Setup

```bash
$ make server          # create all container servers (need only once)
```

You can delete the container servers.

```bash
$ make server-clean    # delete the container servers
```

### 2. TBD

## For Developers

```bash
$ make check          # all static analysis scripts
$ make format         # format scripts
$ make lint           # lints scripts
```
