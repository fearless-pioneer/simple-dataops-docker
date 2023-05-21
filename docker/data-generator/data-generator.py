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
import redis
from sklearn.datasets import load_wine
from time import sleep
from datetime import datetime
from pytz import timezone
import json

REDIS_CLINET = redis.Redis(host="redis", port=6379, db=0)
KR_TZ = timezone("Asia/Seoul")


def main() -> None:
    """Main function."""
    X, y = load_wine(return_X_y=True, as_frame=True)
    cnt = 0
    data_length = X.shape[0]
    while True:
        REDIS_CLINET.set(
            cnt,
            json.dumps(
                {
                    "Time": datetime.now(timezone("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S"),
                    "X": json.dumps(X.iloc[cnt % data_length].to_dict()),
                    "y": str(y.iloc[cnt % data_length]),
                },
            ),
        )
        cnt += 1
        print(f"{cnt} row is pushed...")
        sleep(2)


if __name__ == "__main__":
    main()