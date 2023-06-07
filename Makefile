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
	poetry run pyright
	poetry run ruff src docker --fix

######################
#   docker compose   #
######################
compose:
	make database
	make airflow
	make broker

compose-clean:
	make broker-clean
	make airflow-clean
	make database-clean

database:
	docker compose -p database -f docker-compose-database.yaml up -d

database-clean:
	docker compose -p database down -v
	docker rmi database-data-generator

airflow:
	docker build -t airflow -f docker/airflow/Dockerfile .
	docker compose -p airflow -f docker-compose-airflow.yaml up -d

airflow-clean:
	docker compose -p airflow down -v
	docker rmi airflow
	rm -r ./logs

broker:
	docker compose -p broker -f docker-compose-broker.yaml up -d

broker-clean:
	docker compose -p broker down -v
