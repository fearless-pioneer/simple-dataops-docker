"""Batch glue pipeline."""

from argparse import ArgumentParser

import pymysql
from pymongo import MongoClient
from pymysql.connections import Connection


def create_db_client() -> tuple[MongoClient, Connection]:
    """Create DB client."""
    mongo_client = MongoClient(
        username="mongo",
        password="mongo",
        host="localhost",
        port=27017,
        directConnection=True,
        ssl=False,
    )

    maria_client = pymysql.connect(
        user="maria",
        password="maria",
        host="localhost",
        port=3306,
        database="maria",
    )
    return mongo_client, maria_client


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


def run(start_date: str, mongo_client: MongoClient, maria_client: Connection) -> None:
    """Run main function."""
    # Get wine data collection
    collection = mongo_client["mongo"]["wine_data"]

    # Find new data
    query = {"time": {"$gte": start_date}}
    docs = list(collection.find(query))

    for doc in docs:
        features = eval(doc["input"])
        query = f"""
        INSERT INTO wine_data
            (mongo_id, time, alcohol, malic_acid, ash, alcalinity_of_ash, magnesium,
            total_phenols, flavanoids, nonflavanoid_phenols, proanthocyanins,
            color_intensity, hue, od280_od315_of_diluted_wines, proline, target)
            VALUES (
                "{doc["_id"]}",
                "{doc["time"]}",
                {features["alcohol"]},
                {features["malic_acid"]},
                {features["ash"]},
                {features["alcalinity_of_ash"]},
                {features["magnesium"]},
                {features["total_phenols"]},
                {features["flavanoids"]},
                {features["nonflavanoid_phenols"]},
                {features["proanthocyanins"]},
                {features["color_intensity"]},
                {features["hue"]},
                {features["od280/od315_of_diluted_wines"]},
                {features["proline"]},
                {doc["target"]}
            );
        """

        with maria_client.cursor() as cursor:
            cursor.execute(query)
            maria_client.commit()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--start-date", dest="start_date", type=str, default="2023-06-07 11:52:00")
    args = parser.parse_args()

    mongo_client, maria_client = create_db_client()

    create_table(maria_client=maria_client)

    run(start_date=args.start_date, mongo_client=mongo_client, maria_client=maria_client)
