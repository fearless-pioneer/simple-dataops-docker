# Simple DataOps Docker

[![License: Apache 2.0](https://img.shields.io/badge/license-Apache--2.0-green.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/imports-isort-white)](https://pycqa.github.io/isort)
[![Type Checking: mypy](https://img.shields.io/badge/type%20checking-mypy-red)](https://github.com/python/mypy)
[![Linting: ruff](https://img.shields.io/badge/linting-ruff-purple)](https://github.com/astral-sh/ruff)
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

<p align="center"><img src="asset/landscape.png" width="700"></p>

## Prerequisites

- Install [Docker](https://docs.docker.com/engine/install/).

## Preparation

Install [Python 3.10](https://www.python.org/downloads/release/python-3100/) on [Pyenv](https://github.com/pyenv/pyenv#installation) or [Anaconda](https://docs.anaconda.com/anaconda/install/index.html) and execute the following commands:

```bash
$ make init             # setup packages (need only once)
```

## Infra Setup

```bash
$ make compose          # create all the containers (need only once)
```

You can delete the containers.

```bash
$ make compose-clean    # delete the containers
```

### 1. Mongo DB

You can access `localhost:8081` from a web browser and log in as `admin` for both ID and password and then view the data that is being added to the `mongo` database in the Mongo DB through the data generator.

<p align="center"><img src="asset/mongodb_main_screen.png" width="800"></p>

<p align="center"><img src="asset/mongodb_mongo_database.png" width="800"></p>

### 2. Airflow

You can access `localhost:8008` from a web browser and log in as `admin` for both ID and password.

<p align="center"><img src="asset/airflow_log_in.png" width="800"></p>

<p align="center"><img src="asset/airflow_main_screen.png" width="800"></p>

Run the dags according to the detailed case studies below.

## Case Studies

### 1. Simple Test

You can run on a simple dag called `simple-test` that you see on the main screen of airflow. You can also see the dag in `src/dags/1_simple_test/simple_dag.py`, defined as several tasks with the python and bash operators.

The schedule interval of the dag is `@once`, so when the dag is executed, it only works once at first. (references: [DAG Runs in Airflow](https://airflow.apache.org/docs/apache-airflow/1.10.1/scheduler.html#dag-runs) and [Cron in Wikipedia](https://en.wikipedia.org/wiki/Cron#CRON_expression))

So let's run the dag. You can unpause the dag by clicking `Pause/Unpause DAG`.

<p align="center"><img src="asset/simple_dag_unpause.png" width="250"></p>

After a few seconds, you can confirm that the dag has successfully ended on the main screen of airflow.

<p align="center"><img src="asset/simple_dag_success.png" width="800"></p>

### 2. Batch Glue

You can run a `batch-glue` dag that extracts, transforms, and loads (ETLs) data like [AWS Glue](https://aws.amazon.com/glue). You can also see the dag in `src/dags/2_batch_glue/dag.py` and the code for the task that runs on the bash operator in the dag in `src/dags/2_batch_glue/pipeline.py`.

The task that works in the dag is to extract the wine data in Mongo DB, transform the type of data, and then load it into Maria DB.

The dag runs every minute because the schedule interval for the dag is specified as (*/1 * * * *) every minute. (We don't manually run it.) In other words, the dag ETLs data between Mongo DB and Maria DB every minute.

So let's run the dag. You can unpause the dag by clicking `Pause/Unpause DAG`.

<p align="center"><img src="asset/batch_glue_dag_unpause.png" width="250"></p>

After a few seconds, you can confirm that the dag has successfully ended on the main screen of airflow.

<p align="center"><img src="asset/batch_glue_dag_success.png" width="800"></p>

Finally, you can access Maria DB and see that data is added every time the dag is executed.

```bash
$ docker exec -it mariadb bash
root@742cd8f602a7:/# mariadb -u maria -p
Enter password: maria
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 32
Server version: 10.6.13-MariaDB-1:10.6.13+maria~ubu2004 mariadb.org binary distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> use maria
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
MariaDB [maria]> select * from wine_data limit 5;
+----+---------------------+--------------------------+---------+------------+------+-------------------+-----------+---------------+------------+----------------------+-----------------+-----------------+------+------------------------------+---------+--------+
| id | time                | mongo_id                 | alcohol | malic_acid | ash  | alcalinity_of_ash | magnesium | total_phenols | flavanoids | nonflavanoid_phenols | proanthocyanins | color_intensity | hue  | od280_od315_of_diluted_wines | proline | target |
+----+---------------------+--------------------------+---------+------------+------+-------------------+-----------+---------------+------------+----------------------+-----------------+-----------------+------+------------------------------+---------+--------+
|  1 | 2023-06-17 15:41:11 | 648d5587d7f2b36f4504969c |   14.23 |       1.71 | 2.43 |              15.6 |       127 |           2.8 |       3.06 |                 0.28 |            2.29 |            5.64 | 1.04 |                         3.92 |    1065 |      0 |
|  2 | 2023-06-17 15:41:13 | 648d5589d7f2b36f4504969d |    13.2 |       1.78 | 2.14 |              11.2 |       100 |          2.65 |       2.76 |                 0.26 |            1.28 |            4.38 | 1.05 |                          3.4 |    1050 |      0 |
|  3 | 2023-06-17 15:41:15 | 648d558bd7f2b36f4504969e |   13.16 |       2.36 | 2.67 |              18.6 |       101 |           2.8 |       3.24 |                  0.3 |            2.81 |            5.68 | 1.03 |                         3.17 |    1185 |      0 |
|  4 | 2023-06-17 15:41:17 | 648d558dd7f2b36f4504969f |   14.37 |       1.95 |  2.5 |              16.8 |       113 |          3.85 |       3.49 |                 0.24 |            2.18 |             7.8 | 0.86 |                         3.45 |    1480 |      0 |
|  5 | 2023-06-17 15:41:19 | 648d558fd7f2b36f450496a0 |   13.24 |       2.59 | 2.87 |                21 |       118 |           2.8 |       2.69 |                 0.39 |            1.82 |            4.32 | 1.04 |                         2.93 |     735 |      0 |
+----+---------------------+--------------------------+---------+------------+------+-------------------+-----------+---------------+------------+----------------------+-----------------+-----------------+------+------------------------------+---------+--------+
5 rows in set (0.004 sec)
```

### 3. Batch SQS

You can run a `batch-sqs` dag imitating [AWS SQS](https://aws.amazon.com/ko/sqs/). This process is an example of storing data using [Message Queue](https://en.wikipedia.org/wiki/Message_queue)(MQ).

We used [RabbitMQ](https://www.rabbitmq.com/) as MQ and [MinIO](https://min.io/) as storage. the rest of settings are same of above.

The process consists of two steps:
- First, you can check that data is generated in the Mongo DB every 2 seconds, and that a dag produces the data in the MQ every minute (same as the second case study above) according to the scheduled interval.
- Second, you can check that the consumer consumes the data from MQ and stores it in storage.

In detail, the dag runs every minute because the schedule interval for the dag is specified as (*/1 * * * *) every minute and publishes the data to the RabbitMQ queue. So we can expect that the data will be synchronized every minute between the source DB(MongoDB) and the queue(RabbitMQ).

Let's run the dag. You can unpause the dag by clicking `Pause/Unpause DAG`.

<p align="center"><img src="asset/batch_sqs_dag_unpause.png" width="250"></p>

After a few seconds, you can confirm that the dag has successfully ended on the main screen of airflow.

<p align="center"><img src="asset/batch_sqs_dag_success.png" width="800"></p>

The first step is ended and we can see the result of them by accessing the RabbitMQ console([localhost:15672](localhost:15672)). the ID and Password are set same word `rabbit`.

<p align="center"><img src="asset/batch_sqs_rabbitmq_console.png" width="800"></p>

Then you can also monitor how second step is going on using two methods.

#### 3.1  Docker Logs

```bash
$ docker logs rabbitmq-consumer -f
```

<p align="center"><img src="asset/batch_sqs_docker_logs.png" width="800"></p>

#### 3.2 MinIO Console

You can access `localhost:9900` from the web browser and log in as ID  `minio` and password `minio123`.

<p align="center"><img src="asset/batch_sqs_minio_console.png" width="800"></p>

<br>

Finally, you finished our case studies. We hope you enjoy the journey with case studies.

Thank you for visiting our repository!

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/dongminlee94"><img src="https://avatars.githubusercontent.com/u/29733842?v=4?s=100" width="100px;" alt="Dongmin Lee"/><br /><sub><b>Dongmin Lee</b></sub></a><br /><a href="https://github.com/fearless-pioneer/simple-dataops-docker/commits?author=dongminlee94" title="Documentation">📖</a> <a href="https://github.com/fearless-pioneer/simple-dataops-docker/commits?author=dongminlee94" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Kimdongui"><img src="https://avatars.githubusercontent.com/u/65523228?v=4?s=100" width="100px;" alt="Kim dong hyun, 김동현"/><br /><sub><b>Kim dong hyun, 김동현</b></sub></a><br /><a href="https://github.com/fearless-pioneer/simple-dataops-docker/commits?author=Kimdongui" title="Documentation">📖</a> <a href="https://github.com/fearless-pioneer/simple-dataops-docker/commits?author=Kimdongui" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
