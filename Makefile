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
	poetry run ruff src --fix

######################
#   build image   #
######################
build-image:
	docker build -t simple-dataops-airflow -f Dockerfile .

build-image-clean:
	docker rmi simple-dataops-airflow

######################
#   docker compose   #
######################
compose:
	docker compose up -d

compose-clean:
	docker compose down -v
