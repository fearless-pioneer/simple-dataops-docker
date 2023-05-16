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

####################
#   docker build   #
####################
build:
	docker build --platform linux/amd64 -f Dockerfile -t simple-dataops-airflow:latest .

######################
#   docker compose   #
######################
server:
	docker compose up -d

server-clean:
	docker compose down -v
	docker rmi simple-dataops-k8s-initdb
