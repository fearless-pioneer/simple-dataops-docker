"""Data generator for demo.

Description:
    This script implements data generator for proeject demo.
    1. Load wind dataset from sckit-learn datasets.
    2. Transform single row of wind datasets to JSON format.
    3. Push redis DB via redis python sdk.
    3. Cycle 1-3 infinite steps.

Maintainer:
    Name: Kimdongui
    Email: rkdqus2006@naver.com
"""
import json
from datetime import datetime
from time import sleep

from pymongo import MongoClient
from pymongo.collection import Collection
from pytz import timezone
from sklearn.datasets import load_wine


def create_collection(mongo_client: MongoClient) -> Collection:
    """Create collection."""
    database = mongo_client["mongo"]
    if "wine_data" not in database.list_collection_names():
        database.create_collection("wine_data")
    return database["wine_data"]


def generate_data(collection: Collection) -> None:
    """Generate data."""
    X, y = load_wine(return_X_y=True, as_frame=True)  # noqa: N806
    cnt = 0
    data_length = X.shape[0]
    while True:
        collection.insert_one(
            {
                "Time": datetime.now(timezone("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S"),
                "X": json.dumps(X.iloc[cnt % data_length].to_dict()),
                "y": str(y.iloc[cnt % data_length]),
            },
        )
        cnt += 1
        print(f"{cnt} row is pushed...")
        sleep(2)


if __name__ == "__main__":
    mongo_client = MongoClient(
        username="mongo",
        password="mongo",
        host="mongodb",
        port=27017,
        authSource="admin",
        connectTimeoutMS=60000,
        readPreference="primary",
        directConnection=True,
        ssl=False,
    )
    collection = create_collection(mongo_client=mongo_client)
    generate_data(collection=collection)
