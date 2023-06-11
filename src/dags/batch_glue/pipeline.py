"""Batch glue pipeline."""

from argparse import ArgumentParser
from datetime import datetime, timedelta

import pymysql
from pymongo import MongoClient
from pymysql.connections import Connection


def create_table(maria_client: Connection) -> None:
    """Create table."""
    query = """
    CREATE TABLE IF NOT EXISTS wine_data (
        id INT(10) NOT NULL AUTO_INCREMENT,
        time DATETIME NOT NULL,
        mongo_id VARCHAR(30) NOT NULL,
        alcohol FLOAT(10) NOT NULL,
        malic_acid FLOAT(10) NOT NULL,
        ash FLOAT(10) NOT NULL,
        alcalinity_of_ash FLOAT(10) NOT NULL,
        magnesium FLOAT(10) NOT NULL,
        total_phenols FLOAT(10) NOT NULL,
        flavanoids FLOAT(10) NOT NULL,
        nonflavanoid_phenols FLOAT(10) NOT NULL,
        proanthocyanins FLOAT(10) NOT NULL,
        color_intensity FLOAT(10) NOT NULL,
        hue FLOAT(10) NOT NULL,
        od280_od315_of_diluted_wines FLOAT(10) NOT NULL,
        proline FLOAT(10) NOT NULL,
        target INT NOT NULL,
        PRIMARY KEY (`id`)
    );"""

    with maria_client.cursor() as cursor:
        cursor.execute(query)
        maria_client.commit()


def run(task_time: str, mongo_client: MongoClient, maria_client: Connection) -> None:
    """Run main function."""
    # Construct a start_date from the task_time
    task_time = datetime.fromisoformat(task_time.split("+")[0])
    start_date = str(datetime.strptime(str(task_time), "%Y-%m-%d %H:%M:%S") + timedelta(hours=9))

    # Check if the data exists in mariadb
    cond_query = """
    SELECT count(*) FROM wine_data;
    """
    with maria_client.cursor() as cursor:
        cursor.execute(cond_query)
        data = cursor.fetchone()[0]

    # Get new data
    select_query = {"time": {"$gte": start_date}} if data else {}
    docs = list(mongo_client["mongo"]["wine_data"].find(select_query))

    values = []
    for doc in docs:
        features = eval(doc["features"])
        values.append(
            [
                str(doc["_id"]),
                str(doc["time"]),
                features["alcohol"],
                features["malic_acid"],
                features["ash"],
                features["alcalinity_of_ash"],
                features["magnesium"],
                features["total_phenols"],
                features["flavanoids"],
                features["nonflavanoid_phenols"],
                features["proanthocyanins"],
                features["color_intensity"],
                features["hue"],
                features["od280/od315_of_diluted_wines"],
                features["proline"],
                doc["labels"],
            ],
        )

    insert_query = """
    INSERT INTO wine_data
        (mongo_id, time, alcohol, malic_acid, ash, alcalinity_of_ash, magnesium,
        total_phenols, flavanoids, nonflavanoid_phenols, proanthocyanins,
        color_intensity, hue, od280_od315_of_diluted_wines, proline, target)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    with maria_client.cursor() as cursor:
        cursor.executemany(insert_query, values)
        maria_client.commit()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--task-time", dest="task_time", type=str, default="")
    args = parser.parse_args()

    mongo_client = MongoClient(
        username="mongo",
        password="mongo",
        host="mongodb",
        port=27017,
        directConnection=True,
        ssl=False,
    )

    maria_client = pymysql.connect(
        user="maria",
        password="maria",
        host="mariadb",
        port=3306,
        database="maria",
        charset="utf8",
    )

    create_table(maria_client=maria_client)

    run(task_time=args.task_time, mongo_client=mongo_client, maria_client=maria_client)
