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
from pytz import timezone
from sklearn.datasets import load_wine


def main(mongo_client: MongoClient) -> None:
    """Run main function."""
    # Create a collection
    collection = mongo_client["mongo"]["wine_data"]

    # Load wine dataset
    features, labels = load_wine(return_X_y=True, as_frame=True)

    # Generate data continuously
    cnt = 0
    data_length = features.shape[0]
    while True:
        collection.insert_one(
            {
                "index": cnt,
                "time": datetime.now(timezone("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S"),
                "features": json.dumps(features.iloc[cnt % data_length].to_dict()),
                "labels": str(labels.iloc[cnt % data_length]),
            },
        )
        print(f"{cnt} row is pushed...")

        cnt += 1
        sleep(2)


if __name__ == "__main__":
    mongo_client = MongoClient(
        username="mongo",
        password="mongo",
        host="mongodb",
        port=27017,
        directConnection=True,
        ssl=False,
    )

    main(mongo_client=mongo_client)
