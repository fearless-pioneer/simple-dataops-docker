PROFILE_NAME=simple-dataops-k8s

######################
#   initialization   #
######################
install-poetry:
	@echo "Install poetry";\
	if [ `command -v pip` ];\
		then pip install poetry;\
	else\
		curl -sSL https://install.python-poetry.org | python3 -;\
	fi;

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

###############
#   cluster   #
###############
cluster:
	minikube start --driver=docker --profile $(PROFILE_NAME) --extra-config=kubelet.housekeeping-interval=10s --cpus=max --memory=max
	minikube addons enable metrics-server --profile $(PROFILE_NAME)
	minikube addons list --profile $(PROFILE_NAME)

cluster-clean:
	minikube delete --profile $(PROFILE_NAME)
