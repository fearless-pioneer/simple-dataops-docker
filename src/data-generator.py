"""Data generator for demo.

Description:
    This script implements data generator for proeject demo.
    1. Load wind dataset from sckit-learn datasets.
    2. Transform single row of wind datasets to JSON format.
    3. Push redis stack DB via redis python sdk.
    3. Cycle 1-3 infinite steps.

Maintainer:
    Name: Kimdongui
    Email: rkdqus2006@naver.com
"""
import redis
from sklearn.datasets import load_wine

REDIS_CLINET = redis.Redis(host="localhost", port=6379, db=0)

if __name__ == "__main__":
    X, y = load_wine(return_X_y=True, as_frame=True)
