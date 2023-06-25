######################
#   initialization   #
######################
install-poetry:
	@echo "Install poetry";\
	curl -sSL https://install.python-poetry.org | python3 - --version 1.4.2

init:
	@echo "Construct development environment";\
	if [ -z $(VIRTUAL_ENV) ]; then echo Warning, Virtual Environment is required; fi;\
	if [ -z `command -v poetry` ];\
		then make install-poetry;\
	fi;\
	pip install -U pip
	poetry install
	poetry run pre-commit install

#######################
#   static analysis   #
#######################
check: format lint

format:
	poetry run black .

lint:
	poetry run ruff src docker --fix

######################
#   docker compose   #
######################
compose:
	make db
	make airflow
	make queue

compose-clean:
	make queue-clean
	make airflow-clean
	make db-clean

db:
	docker compose -p db -f docker-compose-db.yaml up -d

db-clean:
	docker compose -p db down -v
	docker rmi db-data-generator

airflow:
	docker build -t airflow -f docker/airflow/Dockerfile .
	docker compose -p airflow -f docker-compose-airflow.yaml up -d

airflow-clean:
	docker compose -p airflow down -v
	docker rmi airflow
	rm -r ./logs

queue:
	docker compose -p queue -f docker-compose-queue.yaml up -d

queue-clean:
	docker compose -p queue down -v
	docker rmi queue-rabbitmq-consumer
