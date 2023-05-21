FROM python:3.10.11-slim

COPY docker/data-generator/data-generator.py data-generator.py

RUN pip install redis scikit-learn pandas

CMD ["python", "data-generator.py"]
